import threading
import time
from typing import Any

import requests


class WeatherCheck(threading.Thread):
    def __init__(
        self,
        city: str,
        api_key: str,
        country_code: str,
        delay: int = 1,
        weather: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(daemon=True)
        self.city = city
        self.api_key = api_key
        self.country_code = country_code
        self.delay = delay
        self.weather = weather if weather is not None else {}
        self._stop_event = threading.Event()

    def _build_url(self) -> str:
        return "https://api.openweathermap.org/data/2.5/weather"

    def _fetch_weather(self) -> dict[str, Any]:
        response = requests.get(
            self._build_url(),
            params={
                "q": f"{self.city},{self.country_code}",
                "appid": self.api_key,
                "units": "metric",
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        return {
            "city": data.get("name", self.city.title()),
            "country": data.get("sys", {}).get("country", self.country_code),
            "temperature_c": data.get("main", {}).get("temp"),
            "feels_like_c": data.get("main", {}).get("feels_like"),
            "humidity": data.get("main", {}).get("humidity"),
            "description": (
                data.get("weather", [{}])[0].get("description", "unknown").title()
            ),
            "updated_at": int(time.time()),
        }

    def stop(self) -> None:
        self._stop_event.set()

    def run(self) -> None:
        while not self._stop_event.is_set():
            try:
                latest_weather = self._fetch_weather()
                self.weather.clear()
                self.weather.update(latest_weather)
            except requests.RequestException as exc:
                self.weather.clear()
                self.weather.update({"error": str(exc), "updated_at": int(time.time())})

            self._stop_event.wait(self.delay)


# Backward compatibility with the original class name from the pasted snippet.
Weather_check = WeatherCheck
