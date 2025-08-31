import requests
import os
import tempfile

def download_file(url):
    filename = url.split("/")[-1]
    temp_dir = tempfile.gettempdir()
    local_path = os.path.join(temp_dir, filename)

    if os.path.exists(local_path):
        return local_path

    try:
        r = requests.get(url, stream=True, timeout=60)
        r.raise_for_status()
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return local_path
    except Exception:
        return None

