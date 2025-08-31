import os
import subprocess
import tempfile
import json
import requests

TWRP_JSON_URL = "https://raw.githubusercontent.com/Android-Artisan/anub1s/refs/heads/main/twrp_recoveries.json"
CACHE_DIR = os.path.join(tempfile.gettempdir(), "anub1s_twrp_cache")
os.makedirs(CACHE_DIR, exist_ok=True)
LOCAL_JSON_PATH = os.path.join(CACHE_DIR, "twrp_recoveries.json")

def update_twrp_json():
    try:
        resp = requests.get(TWRP_JSON_URL, timeout=10)
        if resp.status_code == 200:
            with open(LOCAL_JSON_PATH, "w", encoding="utf-8") as f:
                f.write(resp.text)
            return True
    except Exception as e:
        print(f"[update_twrp_json] Failed to update JSON: {e}")
    return False

def load_twrp_json():
    if not os.path.exists(LOCAL_JSON_PATH):
        if not update_twrp_json():
            return None
    try:
        with open(LOCAL_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[load_twrp_json] JSON load error: {e}")
        return None

def get_twrp_tar_url(device_model):
    data = load_twrp_json()
    if not data:
        print("[get_twrp_tar_url] No JSON data available.")
        return None
    entry = data.get(device_model)
    if not entry:
        print(f"[get_twrp_tar_url] No entry for device: {device_model}")
        return None
    stable_url = entry.get("twrp_images", {}).get("stable")
    return stable_url

def download_twrp_tar(device_model):
    print(f"[download_twrp_tar] Getting TWRP tar URL for device: {device_model}")

    url = get_twrp_tar_url(device_model)
    if not url:
        print(f"[download_twrp_tar] No tar URL found for {device_model}")
        return None

    filename = f"{device_model}_twrp.tar"
    cached_path = os.path.join(CACHE_DIR, filename)

    if os.path.exists(cached_path):
        print(f"[download_twrp_tar] Using cached TWRP tar at {cached_path}")
        return cached_path

    print(f"[download_twrp_tar] Found URL: {url}")
    print(f"[download_twrp_tar] Downloading to: {cached_path}")

    # Use curl to download file
    try:
        cmd = [
            "curl", "-L", "-o", cached_path, url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[download_twrp_tar] curl failed: {result.stderr}")
            if os.path.exists(cached_path):
                os.remove(cached_path)
            return None

        # Check size, must be > 10KB
        if os.path.getsize(cached_path) < 10 * 1024:
            print("[download_twrp_tar] File too small or missing.")
            os.remove(cached_path)
            return None

        return cached_path
    except Exception as e:
        print(f"[download_twrp_tar] Exception: {e}")
        return None

