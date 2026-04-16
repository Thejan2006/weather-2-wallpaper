# Dynamic Weather Wallpaper App

This project is a Python desktop automation app for Windows that checks the live weather of a selected city and updates the desktop wallpaper to match the current weather condition.

The app uses the OpenWeather API to fetch weather data, then generates a local wallpaper image based on the weather description and applies it to the Windows desktop automatically.

## Features

- Fetches live weather data for a selected city
- Runs weather updates in the background
- Changes the Windows wallpaper based on weather conditions
- Generates local wallpaper files automatically
- Uses simple Python modules without heavy dependencies

## Technologies Used

- Python 3
- `requests` for API calls and downloads
- `threading` for background tasks
- `ctypes` for Windows wallpaper updates
- `pathlib` for file handling
- `struct` for generating BMP wallpaper files
- OpenWeather API
- Windows API `SystemParametersInfoW`

## Project Structure

- [main.py](./main.py)  
  Starts the application and runs the weather checker and wallpaper engine.

- [weather_check.py](./weather_check.py)  
  Connects to the OpenWeather API and keeps the latest weather data updated.

- [engine.py](./engine.py)  
  Creates weather-based wallpaper images and sets them as the Windows desktop background.

- [image_download.py](./image_download.py)  
  Utility module for downloading images safely to the `downloads` folder.

- `downloads/`  
  Stores downloaded images and generated wallpaper files.

## How It Works

1. The app starts in `main.py`.
2. `weather_check.py` runs in a background thread and fetches the current weather for the configured city.
3. `engine.py` reads the latest weather description.
4. Based on the weather type such as clear, clouds, rain, or snow, the app creates a matching wallpaper.
5. The wallpaper is applied to the Windows desktop automatically.

## Requirements

- Windows operating system
- Python 3.10 or newer
- Internet connection
- OpenWeather API key

## Installation

1. Clone or download the project.
2. Open a terminal in the project folder:

```powershell
cd "E:\All Projects and Repo\Get weather"
```

3. Install the required package:

```powershell
pip install requests
```

## Configuration

Open [main.py](./main.py) and update these values if needed:

```python
CITY = "kandy"
API_KEY = "your_openweather_api_key"
COUNTRY_CODE = "LK"
```

You can also adjust:

- `WEATHER_REFRESH_SECONDS` to control how often weather data is refreshed
- `WALLPAPER_POLL_SECONDS` to control how often the wallpaper engine checks for changes
- `STATUS_PRINT_SECONDS` to control how often status is printed in the terminal

## Run the App

Use:

```powershell
python main.py
```

The app will continue running until you stop it with `Ctrl+C`.

## Example Output

```text
Starting dynamic weather app!
Wallpaper directory ready at: downloads\wallpapers
Press Ctrl+C to stop the app.
{'city': 'Kandy', 'country': 'LK', 'temperature_c': 28.4, 'feels_like_c': 31.2, 'humidity': 74, 'description': 'Overcast Clouds', 'updated_at': 1776326402}
Wallpaper updated for Overcast Clouds: E:\All Projects and Repo\Get weather\downloads\wallpapers\clouds.bmp
```

## Notes

- The wallpaper update feature is designed for Windows.
- The current project generates simple BMP wallpapers based on weather categories.
- `image_download.py` is available if you want to extend the project to use downloaded weather-themed images instead of generated wallpapers.

## Future Improvements

- Use real background images for each weather type
- Move the API key into environment variables
- Add support for more cities and dynamic configuration
- Add startup support so the app runs automatically when Windows starts
- Build a small GUI for changing settings

## Author

Dynamic Weather Wallpaper App built with Python for live weather-based desktop customization.
