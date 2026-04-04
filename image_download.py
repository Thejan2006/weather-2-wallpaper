from pathlib import Path

import requests


class ImageDownloader:
    def __init__(self, download_dir: str = "downloads") -> None:
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)

    def download(self, url: str, filename: str | None = None) -> Path:
        target_name = filename or url.rstrip("/").split("/")[-1] or "image.bin"
        target_path = self.download_dir / target_name

        response = requests.get(url, timeout=20)
        response.raise_for_status()
        target_path.write_bytes(response.content)
        return target_path
