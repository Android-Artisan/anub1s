import os
import platform
import stat
import zipfile
from shutil import which

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
HEIMDAL_DIR = os.path.join(ROOT_DIR, "heimdal")
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".anub1s_tools")
os.makedirs(CACHE_DIR, exist_ok=True)

def is_executable(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)

def find_executable(name):
    path = which(name)
    return path if path and is_executable(path) else None

def make_executable(path):
    if platform.system() != "Windows":
        os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)

def get_adb_path():
    adb_name = "adb.exe" if platform.system() == "Windows" else "adb"
    return find_executable(adb_name)

def extract_zip(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
        return True
    except Exception as e:
        print("Error extracting zip:", e)
        return False

def get_heimdall_path():
    system = platform.system()
    archive_map = {
        "Linux": "linux-build.zip",
        "Windows": "win64-build.zip",
        "Darwin": "macos-build.zip"
    }

    heimdall_name = "heimdall.exe" if system == "Windows" else "heimdall"
    archive_name = archive_map.get(system)
    if not archive_name:
        print("Unsupported OS for Heimdall.")
        return None

    zip_path = os.path.join(HEIMDAL_DIR, archive_name)
    if not os.path.exists(zip_path):
        print(f"Missing local Heimdall archive: {zip_path}")
        return None

    extract_dir = os.path.join(CACHE_DIR, f"heimdall-{system.lower()}")
    heimdall_path = os.path.join(extract_dir, heimdall_name)

    if not os.path.exists(heimdall_path):
        os.makedirs(extract_dir, exist_ok=True)
        if not extract_zip(zip_path, extract_dir):
            return None

    if os.path.exists(heimdall_path):
        make_executable(heimdall_path)
        return heimdall_path
    return None

def ensure_adb_and_heimdall():
    adb = get_adb_path()
    heimdall = get_heimdall_path()

    if not adb:
        return False, "ADB not found in PATH."
    if not heimdall:
        return False, "Heimdall not found or failed to extract."
    return True, "ADB and Heimdall are ready."

