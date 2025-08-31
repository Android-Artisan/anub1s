import os
import subprocess
import tarfile
import tempfile
from utils.adb_heimdall_manager import get_adb_path, get_heimdall_path

def create_recovery_tar(image_path):
    """
    Packages recovery.img into recovery.tar suitable for Heimdall flashing.
    """
    temp_dir = tempfile.gettempdir()
    tar_path = os.path.join(temp_dir, "recovery.tar")

    try:
        with tarfile.open(tar_path, "w") as tar:
            tar.add(image_path, arcname="recovery.img")
        return tar_path
    except Exception:
        return None

def flash_recovery_with_heimdall(image_path):
    """
    Flash TWRP recovery using Heimdall.
    """
    adb_path = get_adb_path()
    heimdall_path = get_heimdall_path()
    if not adb_path or not heimdall_path:
        return False, "ADB or Heimdall not found."

    tar_path = create_recovery_tar(image_path)
    if not tar_path or not os.path.exists(tar_path):
        return False, "Failed to create recovery tar archive."

    try:
        # Reboot device into download mode
        subprocess.check_call([adb_path, "reboot", "download"])

        # Heimdall flash recovery.tar to recovery partition
        # The standard command for flashing recovery with heimdall is:
        # heimdall flash --RECOVERY recovery.img
        # But Heimdall requires the image, not the tar.
        # So alternatively, we just flash the recovery.img directly:
        recovery_img_path = image_path

        # Wait a few seconds to ensure device is in download mode (optional)
        import time
        time.sleep(8)

        # Flash recovery partition using Heimdall
        subprocess.check_call([
            heimdall_path, "flash", "--recovery", recovery_img_path, "--no-reboot"
        ])

        # Reboot device
        subprocess.check_call([adb_path, "reboot"])

        return True, "Successfully flashed recovery."
    except subprocess.CalledProcessError as e:
        return False, f"Flashing failed: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"

