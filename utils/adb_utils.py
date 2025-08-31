import subprocess
import json

def get_device_info():
    """
    Returns device info dict if Samsung device connected via adb, else None.
    """
    try:
        # Check connected devices
        devices_output = subprocess.check_output(['adb', 'devices']).decode()
        lines = devices_output.strip().splitlines()
        if len(lines) <= 1:
            return None
        # Assume first device listed is target
        device_line = lines[1]
        if "device" not in device_line:
            return None

        # Get device model
        model = subprocess.check_output(['adb', 'shell', 'getprop', 'ro.product.model']).decode().strip()
        manufacturer = subprocess.check_output(['adb', 'shell', 'getprop', 'ro.product.manufacturer']).decode().strip()
        if "samsung" not in manufacturer.lower():
            return None

        # Get Android and One UI versions
        android_version = subprocess.check_output(['adb', 'shell', 'getprop', 'ro.build.version.release']).decode().strip()
        oneui_version = subprocess.check_output(['adb', 'shell', 'getprop', 'ro.build.version.oneui']).decode().strip()
        chipset = subprocess.check_output(['adb', 'shell', 'getprop', 'ro.board.platform']).decode().strip()

        return {
            "device": model,
            "manufacturer": manufacturer,
            "android_version": android_version,
            "oneui_version": oneui_version,
            "chipset": chipset
        }
    except Exception:
        return None

