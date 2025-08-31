import requests

ROM_LIST_URL = "https://raw.githubusercontent.com/Android-Artisan/anub1s/refs/heads/main/official_roms.json"

def get_official_roms_for_device(device_model):
    model = device_model.upper().replace(" ", "")
    try:
        response = requests.get(ROM_LIST_URL)
        if response.status_code != 200:
            print(f"Failed to fetch ROM list: {response.status_code}")
            return []

        rom_data = response.json()
        return rom_data.get(model, [])
    except Exception as e:
        print(f"Error fetching ROM list: {e}")
        return []
