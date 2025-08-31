import subprocess

def run_adb_command(cmd):
    try:
        result = subprocess.check_output(["adb"] + cmd, stderr=subprocess.DEVNULL)
        return result.decode().strip()
    except:
        return ""

def is_device_connected():
    return "device" in run_adb_command(["devices"])

def get_device_info():
    if not is_device_connected():
        return None

    manufacturer = run_adb_command(["shell", "getprop", "ro.product.manufacturer"])
    if "samsung" not in manufacturer.lower():
        return None

    return {
        "model": run_adb_command(["shell", "getprop", "ro.product.model"]),
        "device": run_adb_command(["shell", "getprop", "ro.product.device"]),
        "chip": run_adb_command(["shell", "getprop", "ro.chipname"]),
        "oneui": run_adb_command(["shell", "getprop", "ro.build.version.oneui"]),
    }
