import subprocess
import os

def run_cmd(cmd):
    """
    Run a shell command and return (success, output).
    """
    try:
        result = subprocess.run(cmd, shell=False, capture_output=True, text=True, timeout=300)
        success = (result.returncode == 0)
        return success, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)


def flash_recovery_img(img_path: str) -> bool:
    """
    Flash the given recovery image to the device via adb and fastboot.
    Returns True on success, False on failure.
    """
    if not os.path.isfile(img_path):
        print(f"Recovery image not found: {img_path}")
        return False

    # Reboot device to bootloader/fastboot mode
    success, out = run_cmd(["adb", "reboot", "bootloader"])
    if not success:
        print("Failed to reboot device to bootloader mode:\n", out)
        return False

    # Wait a bit for bootloader to come up
    import time
    time.sleep(5)

    # Flash recovery image
    success, out = run_cmd(["fastboot", "flash", "recovery", img_path])
    if not success:
        print("Failed to flash recovery image:\n", out)
        return False

    # Reboot device
    success, out = run_cmd(["fastboot", "reboot"])
    if not success:
        print("Failed to reboot device after flashing recovery:\n", out)
        return False

    print("Recovery image flashed successfully.")
    return True


def flash_zip_rom(zip_path: str) -> bool:
    """
    Sideload the ROM zip file via adb.
    Assumes device is already in recovery sideload mode.
    Returns True on success, False on failure.
    """

    if not os.path.isfile(zip_path):
        print(f"ROM zip file not found: {zip_path}")
        return False

    print("Please boot your device into recovery sideload mode now.")

    # You can optionally add a dialog/wait here if needed.

    # Run adb sideload
    success, out = run_cmd(["adb", "sideload", zip_path])
    if not success:
        print("Failed to sideload ROM:\n", out)
        return False

    print("ROM sideloaded successfully.")
    return True
