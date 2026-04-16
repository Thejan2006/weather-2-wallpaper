from pathlib import Path
from urllib.parse import unquote, urlsplit

import requests

DEFAULT_IMAGE_URL = "https://images.unsplash.com/photo-1721793958693-d468a0ad0fdf?q=80&w=737&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"

CONTENT_TYPE_TO_SUFFIX = {
    "image/gif": ".gif",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


class ImageDownloader:
    def __init__(self, download_dir: str = "downloads") -> None:
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)

    def _build_target_name(
        self,
        url: str,
        filename: str | None,
        content_type: str,
    ) -> str:
        if filename:
            raw_name = Path(filename).name
        else:
            raw_name = Path(unquote(urlsplit(url).path)).name or "image"

        safe_name = "".join(
            "_" if char in '<>:"/\\|?*' else char for char in raw_name
        ).strip(" .")
        safe_name = safe_name or "image"

        if Path(safe_name).suffix:
            return safe_name

        suffix = CONTENT_TYPE_TO_SUFFIX.get(content_type, ".bin")
        return f"{safe_name}{suffix}"

    def download(self, url: str, filename: str | None = None) -> Path:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
        target_name = self._build_target_name(url, filename, content_type)
        target_path = self.download_dir / target_name

        target_path.write_bytes(response.content)
        return target_path
        
        
        
        






        
