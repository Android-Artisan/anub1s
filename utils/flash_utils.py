import subprocess
import shutil
import os

def get_heimdall_path():
    # Assume heimdall binary is included or in PATH, customize as needed
    heimdall_bin = shutil.which("heimdall")
    if heimdall_bin:
        return heimdall_bin
    # Fallback, e.g., local bundled heimdall path
    # return "/path/to/heimdall"
    return None

def reboot_to_download_mode():
    # Using adb to reboot to download mode
    try:
        res = subprocess.run(["adb", "reboot", "download"], capture_output=True)
        return res.returncode == 0
    except Exception as e:
        print(f"[reboot_to_download_mode] Exception: {e}")
        return False

def flash_recovery_with_heimdall(heimdall_path, tar_path):
    """
    Flash the recovery tar file using heimdall.
    Extract the recovery.img from tar and flash only recovery partition.
    """

    import tarfile
    import tempfile

    if not os.path.exists(tar_path):
        return False, "Recovery tar file not found."

    try:
        with tarfile.open(tar_path) as tar:
            recovery_img = None
            for member in tar.getmembers():
                if member.name.endswith("recovery.img"):
                    recovery_img = member
                    break
            if not recovery_img:
                return False, "No recovery.img found inside tar."

            with tempfile.TemporaryDirectory() as tmpdir:
                tar.extract(recovery_img, path=tmpdir)
                recovery_img_path = os.path.join(tmpdir, recovery_img.name)
                cmd = [heimdall_path, "flash", "--recovery", recovery_img_path, "--no-reboot"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    return True, "Flashing completed successfully. Reboot device manually."
                else:
                    return False, f"Heimdall flash failed: {result.stderr}"
    except Exception as e:
        return False, f"Exception during flashing: {e}"

