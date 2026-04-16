import ctypes
import struct
import threading
from pathlib import Path
from typing import Any

SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDWININICHANGE = 0x02

WEATHER_PALETTES = {
    "clear": ((49, 124, 212), (255, 204, 92)),
    "clouds": ((88, 102, 122), (198, 206, 214)),
    "rain": ((39, 58, 84), (110, 142, 176)),
    "drizzle": ((74, 102, 128), (155, 182, 198)),
    "thunderstorm": ((18, 25, 43), (86, 96, 118)),
    "snow": ((210, 226, 240), (249, 251, 255)),
    "mist": ((125, 142, 156), (199, 207, 215)),
    "unknown": ((84, 102, 122), (172, 184, 196)),
}

WEATHER_KEYWORDS = {
    "thunderstorm": ("thunder", "storm"),
    "drizzle": ("drizzle",),
    "rain": ("rain", "shower"),
    "snow": ("snow", "sleet", "blizzard"),
    "mist": ("mist", "fog", "haze", "smoke", "dust", "sand", "ash"),
    "clouds": ("cloud", "overcast"),
    "clear": ("clear", "sun", "fair"),
}


class WallpaperChanger(threading.Thread):
    def __init__(
        self,
        weather: dict[str, Any],
        output_dir: str = "downloads/wallpapers",
        delay: int = 5,
    ) -> None:
        super().__init__(daemon=True)
        self.weather = weather
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.delay = delay
        self._stop_event = threading.Event()
        self._last_signature: tuple[str, str] | None = None

    def stop(self) -> None:
        self._stop_event.set()

    def _category_for_description(self, description: str) -> str:
        lowered = description.lower()
        for category, keywords in WEATHER_KEYWORDS.items():
            if any(keyword in lowered for keyword in keywords):
                return category
        return "unknown"

    def _build_wallpaper_path(self, category: str) -> Path:
        return (self.output_dir / f"{category}.bmp").resolve()

    def _interpolate_color(
        self,
        start: tuple[int, int, int],
        end: tuple[int, int, int],
        ratio: float,
    ) -> tuple[int, int, int]:
        return tuple(
            round(start[index] + (end[index] - start[index]) * ratio)
            for index in range(3)
        )

    def _write_gradient_bmp(
        self,
        target_path: Path,
        top_color: tuple[int, int, int],
        bottom_color: tuple[int, int, int],
        width: int = 1920,
        height: int = 1080,
    ) -> None:
        row_size = width * 3
        padding = (4 - row_size % 4) % 4
        pixel_data_size = (row_size + padding) * height
        file_size = 14 + 40 + pixel_data_size

        with target_path.open("wb") as wallpaper_file:
            wallpaper_file.write(b"BM")
            wallpaper_file.write(struct.pack("<IHHI", file_size, 0, 0, 54))
            wallpaper_file.write(
                struct.pack(
                    "<IIIHHIIIIII",
                    40,
                    width,
                    height,
                    1,
                    24,
                    0,
                    pixel_data_size,
                    2835,
                    2835,
                    0,
                    0,
                )
            )

            for row in range(height):
                ratio = row / max(height - 1, 1)
                red, green, blue = self._interpolate_color(
                    bottom_color,
                    top_color,
                    ratio,
                )
                pixel = bytes((blue, green, red))
                wallpaper_file.write(pixel * width)
                if padding:
                    wallpaper_file.write(b"\x00" * padding)

    def _ensure_wallpaper_file(self, category: str) -> Path:
        wallpaper_path = self._build_wallpaper_path(category)
        if wallpaper_path.exists():
            return wallpaper_path

        top_color, bottom_color = WEATHER_PALETTES.get(
            category,
            WEATHER_PALETTES["unknown"],
        )
        self._write_gradient_bmp(wallpaper_path, top_color, bottom_color)
        return wallpaper_path

    def _set_wallpaper(self, image_path: Path) -> None:
        result = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER,
            0,
            str(image_path),
            SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE,
        )
        if not result:
            raise ctypes.WinError()

    def run(self) -> None:
        while not self._stop_event.is_set():
            snapshot = dict(self.weather)
            description = str(snapshot.get("description", "")).strip()

            if snapshot.get("error"):
                print(f"Wallpaper update skipped: {snapshot['error']}")
            elif description:
                category = self._category_for_description(description)
                signature = (category, description)

                if signature != self._last_signature:
                    wallpaper_path = self._ensure_wallpaper_file(category)
                    try:
                        self._set_wallpaper(wallpaper_path)
                        self._last_signature = signature
                        print(
                            f"Wallpaper updated for {description}: {wallpaper_path}"
                        )
                    except OSError as exc:
                        print(f"Failed to update wallpaper: {exc}")

            self._stop_event.wait(self.delay)
