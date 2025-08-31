import requests
from bs4 import BeautifulSoup
import webbrowser

def search_twrp_download(model):
    print(f"Searching TWRP for model: {model}")
    model = model.lower().replace(" ", "")
    base_url = "https://twrp.me"
    devices_page = f"{base_url}/Devices/"

    try:
        response = requests.get(devices_page, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)

        for link in links:
            href = link['href']
            if "/Devices/" in href and model in href.lower():
                full_link = base_url + href
                print(f"Opening TWRP download page: {full_link}")
                webbrowser.open(full_link)
                return

        print("No TWRP recovery found for this model.")
    except Exception as e:
        print(f"Error fetching TWRP data: {e}")
