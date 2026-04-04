import time

import image_downlad
import weather_check


CITY = "colombo"
API_KEY = "e813e05e3126dc4400acb7f4e624f521"
COUNTRY_CODE = "LK"


def main() -> None:
    weather = {}

    print("Starting dynamic weather app!")
    weather_engine = weather_check.WeatherCheck(
        city=CITY,
        api_key=API_KEY,
        country_code=COUNTRY_CODE,
        delay=1,
        weather=weather,
    )
    weather_engine.start()

    downloader = image_downlad.ImageDownloader()
    print(f"Image directory ready at: {downloader.download_dir}")

    try:
        for _ in range(5):
            print(weather)
            time.sleep(1)
    finally:
        weather_engine.stop()
        weather_engine.join(timeout=5)


if __name__ == "__main__":
    main()
