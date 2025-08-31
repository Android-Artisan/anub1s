import subprocess

def flash_recovery_img(img_path):
    try:
        subprocess.call(["adb", "reboot", "bootloader"])
        input("Once in bootloader mode, press Enter to flash recovery...")
        subprocess.call(["fastboot", "flash", "recovery", img_path])
        print("TWRP successfully flashed.")
    except Exception as e:
        print(f"Flash error: {e}")
