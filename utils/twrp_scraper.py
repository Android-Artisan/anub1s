import requests
import os
import tempfile

TWRP_JSON_URL = "https://raw.githubusercontent.com/Android-Artisan/anub1s/refs/heads/main/twrp_recoveries.json"

def get_twrp_links(device_model: str):
    try:
        resp = requests.get(TWRP_JSON_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        devices = data.get("devices", {})
        device_data = devices.get(device_model.upper())
        if not device_data:
            return {}
        return device_data.get("twrp_images", {})
    except Exception:
        return {}

def download_twrp_image(device_model: str, variant="stable") -> str | None:
    links = get_twrp_links(device_model)
    if variant not in links:
        return None

    url = links[variant]
    filename = url.split("/")[-1]
    temp_dir = tempfile.gettempdir()
    local_path = os.path.join(temp_dir, filename)

    if not os.path.exists(local_path):
        try:
            r = requests.get(url, stream=True, timeout=60)
            r.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        except Exception:
            return None

    return local_path

