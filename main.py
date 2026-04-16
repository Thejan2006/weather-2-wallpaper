import time

import image_download
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

    downloader = image_download.ImageDownloader()
    print(f"Image directory ready at: {downloader.download_dir}")
    print("Downloading image...")
    downloaded_image = downloader.download(image_download.DEFAULT_IMAGE_URL)
    print(f"Image download complete: {downloaded_image}")

    try:
        for _ in range(2):
            print(weather)
            time.sleep(1)
    finally:
        weather_engine.stop()
        weather_engine.join(timeout=2)


if __name__ == "__main__":
    main()
