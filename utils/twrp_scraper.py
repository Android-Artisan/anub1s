import requests
from bs4 import BeautifulSoup
import os

def download_twrp_image(model, download_dir="downloads"):
    model = model.lower().replace(" ", "")
    base_url = "https://twrp.me"
    devices_page = f"{base_url}/Devices/"

    try:
        print(f"Searching TWRP for: {model}")
        page = requests.get(devices_page)
        soup = BeautifulSoup(page.text, "html.parser")

        links = soup.find_all("a", href=True)
        match = None

        for link in links:
            href = link["href"]
            if "/Devices/" in href and model in href.lower():
                match = href
                break

        if not match:
            print("No matching TWRP device page found.")
            return None

        device_url = base_url + match
        print(f"Found TWRP device page: {device_url}")

        device_page = requests.get(device_url)
        soup = BeautifulSoup(device_page.text, "html.parser")
        img_link = None

        for a in soup.find_all("a", href=True):
            if a["href"].endswith(".img") and "twrp" in a["href"]:
                img_link = a["href"]
                break

        if not img_link:
            print("No .img file found.")
            return None

        img_url = base_url + img_link if img_link.startswith("/") else img_link
        os.makedirs(download_dir, exist_ok=True)
        local_path = os.path.join(download_dir, os.path.basename(img_url))

        print(f"Downloading TWRP from {img_url} ...")
        r = requests.get(img_url, stream=True)
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

        print(f"Downloaded TWRP to {local_path}")
        return local_path

    except Exception as e:
        print(f"Error: {e}")
        return None
