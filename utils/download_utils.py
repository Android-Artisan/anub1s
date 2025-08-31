import requests
import os
import tempfile

def download_file(url: str) -> str | None:
    """
    Download the file from the given URL to a temp directory.
    Returns the local path if successful, None otherwise.
    """

    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        # Extract filename from URL or default to "downloaded.zip"
        filename = url.split("/")[-1] or "downloaded.zip"

        # Create temp file path
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, filename)

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return file_path
    except Exception as e:
        print(f"Download failed: {e}")
        return None
