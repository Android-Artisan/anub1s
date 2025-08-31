import subprocess
import os

def flash_recovery_img(image_path):
    """
    Flash recovery image via adb/fastboot.
    Returns True if successful.
    """
    try:
        # Reboot device to recovery
        subprocess.check_call(['adb', 'reboot', 'bootloader'])
        subprocess.check_call(['fastboot', 'flash', 'recovery', image_path])
        subprocess.check_call(['fastboot', 'reboot'])
        return True
    except Exception:
        return False

def flash_zip_rom(zip_path):
    """
    Flash ROM ZIP via adb sideload.
    Returns True if successful.
    """
    try:
        subprocess.check_call(['adb', 'reboot', 'recovery'])
        subprocess.check_call(['adb', 'sideload', zip_path])
        return True
    except Exception:
        return False

