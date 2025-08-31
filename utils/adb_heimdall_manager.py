import os
import sys
import platform
import shutil
import zipfile
import tarfile
import requests
import stat

CACHE_DIR = os.path.join(os.path.expanduser("~"), ".anub1s_tools")
os.makedirs(CACHE_DIR, exist_ok=True)

def is_executable(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)

def find_executable(name):
    """Try system PATH first"""
    from shutil import which
    path = which(name)
    if path and is_executable(path):
        return path
    return None

def download_file(url, dest):
    try:
        r = requests.get(url, stream=True, timeout=60)
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    except Exception:
        return False

def make_executable(path):
    if platform.system() != "Windows":
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC)

def get_adb_path():
    adb_name = "adb.exe" if platform.system() == "Windows" else "adb"
    adb_path = find_executable(adb_name)
    if adb_path:
        return adb_path

    # Not found, download and extract
    url = None
    if platform.system() == "Windows":
        url = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
    elif platform.system() == "Darwin":
        url = "https://dl.google.com/android/repository/platform-tools-latest-darwin.zip"
    elif platform.system() == "Linux":
        url = "https://dl.google.com/android/repository/platform-tools-latest-linux.zip"
    else:
        return None

    zip_path = os.path.join(CACHE_DIR, "platform-tools.zip")
    if not os.path.exists(zip_path):
        if not download_file(url, zip_path):
            return None

    extract_dir = os.path.join(CACHE_DIR, "platform-tools")
    if not os.path.exists(extract_dir):
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(CACHE_DIR)

    possible_path = os.path.join(extract_dir, adb_name)
    if os.path.exists(possible_path):
        make_executable(possible_path)
        return possible_path

    return None

def get_heimdall_path():
    heimdall_name = "heimdall.exe" if platform.system() == "Windows" else "heimdall"
    heimdall_path = find_executable(heimdall_name)
    if heimdall_path:
        return heimdall_path

    # Download heimdall binaries from a reliable source or pre-hosted URL
    # (For demo: GitHub releases or your own hosting)
    url = None
    system = platform.system()
    arch = platform.machine()

    if system == "Windows":
        url = "https://github.com/Benjamin-Dobell/Heimdall/releases/download/v1.4.2/Heimdall-v1.4.2-win64.zip"
    elif system == "Linux":
        # Check arch for amd64 vs arm64 - here simplified
        url = "https://github.com/Benjamin-Dobell/Heimdall/releases/download/v1.4.2/heimdall-linux-1.4.2.tar.gz"
    elif system == "Darwin":
        url = "https://github.com/Benjamin-Dobell/Heimdall/releases/download/v1.4.2/heimdall-mac-1.4.2.tar.gz"
    else:
        return None

    archive_path = os.path.join(CACHE_DIR, "heimdall_archive")
    if not os.path.exists(archive_path):
        archive_path += ".zip" if system == "Windows" else ".tar.gz"
        if not download_file(url, archive_path):
            return None

    extract_dir = os.path.join(CACHE_DIR, "heimdall")
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir, exist_ok=True)
        try:
            if archive_path.endswith(".zip"):
                with zipfile.ZipFile(archive_path, "r") as zip_ref:
                    zip_ref.extractall(extract_dir)
            else:
                import tarfile
                with tarfile.open(archive_path, "r:gz") as tar_ref:
                    tar_ref.extractall(extract_dir)
        except Exception:
            return None

    # Find heimdall binary inside extract_dir recursively
    for root, dirs, files in os.walk(extract_dir):
        if heimdall_name in files:
            path = os.path.join(root, heimdall_name)
            make_executable(path)
            return path

    return None

