import subprocess

def run_adb_command(args: list[str]) -> str | None:
    """Run adb command with given args and return stdout if successful, else None."""
    try:
        result = subprocess.run(["adb"] + args, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception as e:
        print(f"[run_adb_command] Exception: {e}")
        return None

def get_device_info() -> dict | None:
    """
    Get basic info about connected device via adb.
    Returns dict with keys: device, chipset, oneui_version or None if no device.
    """
    device = run_adb_command(["shell", "getprop", "ro.product.device"])
    if not device:
        return None

    chipset = run_adb_command(["shell", "getprop", "ro.board.platform"]) or "Unknown"
    oneui_ver = run_adb_command(["shell", "getprop", "ro.build.version.oneui"])

    return {
        "device": device,
        "chipset": chipset,
        "oneui_version": oneui_ver if oneui_ver else "",
    }

