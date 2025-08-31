import requests
import os

def download_file_with_progress(url, dest_path, progress_callback=None):
    try:
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            downloaded = 0
            with open(dest_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback and total > 0:
                            percent = int((downloaded / total) * 100)
                            progress_callback(percent)
        return True, "Download complete."
    except Exception as e:
        return False, f"Download error: {e}"

