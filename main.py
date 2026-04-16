import time

import engine
import weather_check
 

CITY = "kandy"
API_KEY = "e813e05e3126dc4400acb7f4e624f521"
COUNTRY_CODE = "LK"
WEATHER_REFRESH_SECONDS = 300
WALLPAPER_POLL_SECONDS = 5
STATUS_PRINT_SECONDS = 10


def main() -> None:
    weather = {}

    print("Starting dynamic weather app!")
    weather_engine = weather_check.WeatherCheck(
        city=CITY,
        api_key=API_KEY,
        country_code=COUNTRY_CODE,
        delay=WEATHER_REFRESH_SECONDS,
        weather=weather,
    )
    weather_engine.start()

    wallpaper_engine = engine.WallpaperChanger(
        weather=weather,
        delay=WALLPAPER_POLL_SECONDS,
    )
    wallpaper_engine.start()
    print(f"Wallpaper directory ready at: {wallpaper_engine.output_dir}")
    print("Press Ctrl+C to stop the app.")

    try:
        while True:
            if weather:
                print(weather)
            else:
                print("Waiting for weather data...")
            time.sleep(STATUS_PRINT_SECONDS)
    except KeyboardInterrupt:
        print("\nStopping dynamic weather app...")
    finally:
        wallpaper_engine.stop()
        weather_engine.stop()
        wallpaper_engine.join(timeout=5)
        weather_engine.join(timeout=5)


if __name__ == "__main__":
    main()
