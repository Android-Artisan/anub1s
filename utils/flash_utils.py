import subprocess
import shutil
import os

def get_heimdall_path():
    # Assume heimdall binary is included or in PATH, customize as needed
    # Use bundled heimdall binary from heimdal/ directory
    import platform
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(base_dir, '..'))
    heimdal_dir = os.path.join(root_dir, "heimdal")
    if platform.system() == "Linux":
        heimdall_bin = os.path.join(heimdal_dir, "linux-build.zip")
    elif platform.system() == "Darwin":
        heimdall_bin = os.path.join(heimdal_dir, "macos-build.zip")
    elif platform.system() == "Windows":
        heimdall_bin = os.path.join(heimdal_dir, "win64-build.zip")
    else:
        heimdall_bin = shutil.which("heimdall")
    # If the binary is a zip, extract it first
    if heimdall_bin and heimdall_bin.endswith('.zip'):
        import zipfile
        extract_dir = os.path.join(heimdal_dir, "extracted")
        os.makedirs(extract_dir, exist_ok=True)
        with zipfile.ZipFile(heimdall_bin, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        # Find heimdall binary inside extracted dir
        for root, dirs, files in os.walk(extract_dir):
            for f in files:
                if f == "heimdall" or f == "heimdall.exe":
                    return os.path.join(root, f)
        return None
    elif heimdall_bin:
        return heimdall_bin
    else:
        return shutil.which("heimdall")

def reboot_to_download_mode():
    # Using adb to reboot to download mode
    try:
        res = subprocess.run(["adb", "reboot", "download"], capture_output=True)
        return res.returncode == 0
    except Exception as e:
        print(f"[reboot_to_download_mode] Exception: {e}")
        return False

def flash_recovery_with_heimdall(heimdall_path, tar_path):
    import subprocess
    import os
    import tarfile
    import tempfile
    if not os.path.exists(heimdall_path):
        return False, "Heimdall binary not found."
    if not os.path.exists(tar_path):
        return False, "TWRP tar file not found."
    try:
    # Removed unreachable and stray code after main implementation
                img_path = os.path.join(tmpdir, "recovery.img")
                with open(lz4_path, "wb") as f:
                    f.write(tar.extractfile(recovery_lz4).read())
                # Decompress lz4 to img
                decompress_result = subprocess.run(["lz4", "-d", lz4_path, img_path], capture_output=True, text=True)
                if decompress_result.returncode != 0:
                    return False, f"lz4 decompression failed: {decompress_result.stderr}"
                # Flash recovery.img
                result = subprocess.run([
                    heimdall_path, "flash", "--RECOVERY", img_path, "--no-reboot"
                ], capture_output=True, text=True, timeout=120)
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                if result.returncode == 0:
                    return True, "Flashed successfully."
                else:
                    return False, f"Error: {result.stderr or result.stdout}"
    except Exception as e:
        return False, str(e)
    except Exception as e:
        return False, f"Exception during flashing: {e}"

def flash_zip_rom(zip_path):
    """
    Flash a ROM zip file using adb sideload.
    Returns True if successful, False otherwise.
    """
    import os
    import subprocess
    if not os.path.exists(zip_path):
        print("[flash_zip_rom] ROM zip file not found.")
        try:
            print(f"Using heimdall binary: {heimdall_path}")
            print(f"Using TWRP tar: {tar_path}")
            with tarfile.open(tar_path) as tar:
                recovery_lz4 = None
                for member in tar.getmembers():
                    if member.name.endswith("recovery.img.lz4"):
                        recovery_lz4 = member
                        break
                if not recovery_lz4:
                    print("No recovery.img.lz4 found in tar.")
                    return False, "No recovery.img.lz4 found in tar."
                with tempfile.TemporaryDirectory() as tmpdir:
                    lz4_path = os.path.join(tmpdir, "recovery.img.lz4")
                    img_path = os.path.join(tmpdir, "recovery.img")
                    with open(lz4_path, "wb") as f:
                        f.write(tar.extractfile(recovery_lz4).read())
                    print(f"Extracted lz4 to: {lz4_path}")
                    print(f"Will decompress to: {img_path}")
                    # Decompress lz4 to img
                    decompress_result = subprocess.run(["lz4", "-d", lz4_path, img_path], capture_output=True, text=True)
                    print("lz4 STDOUT:", decompress_result.stdout)
                    print("lz4 STDERR:", decompress_result.stderr)
                    if decompress_result.returncode != 0:
                        print(f"lz4 decompression failed: {decompress_result.stderr}")
                        return False, f"lz4 decompression failed: {decompress_result.stderr}"
                    print(f"Decompressed image path: {img_path}")
                    # Flash recovery.img
                    print(f"Running heimdall command: {heimdall_path} flash --RECOVERY {img_path} --no-reboot")
                    result = subprocess.run([
                        heimdall_path, "flash", "--RECOVERY", img_path, "--no-reboot"
                    ], capture_output=True, text=True, timeout=120)
                    print("heimdall STDOUT:", result.stdout)
                    print("heimdall STDERR:", result.stderr)
                    if result.returncode == 0:
                        print("Flashed successfully.")
                        return True, "Flashed successfully."
                    else:
                        print(f"Error: {result.stderr or result.stdout}")
                        return False, f"Error: {result.stderr or result.stdout}"
        except Exception as e:
            print(f"Exception during flashing: {e}")
            return False, str(e)

