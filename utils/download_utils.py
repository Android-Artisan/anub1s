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

def download_file(url):
    """
    Download a file from the given URL to a temp directory.
    Returns the local file path if successful, else None.
    """
    import tempfile
    import os

    filename = url.split("/")[-1]
    dest_path = os.path.join(tempfile.gettempdir(), filename)
    success, msg = download_file_with_progress(url, dest_path)
    if success:
        return dest_path
    else:
        print(f"[download_file] {msg}")
        return None

