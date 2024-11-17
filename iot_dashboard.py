import requests
import datetime

API_URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": 40.7128,  # New York latitude
    "longitude": -74.0060,  # New York longitude
    "current_weather": True,
    "hourly": "temperature_2m,humidity_2m,precipitation,cloudcover,visibility,uv_index,pressure"
}

def fetch_iot_data():
    """Fetches IoT data from the API."""
    try:
        response = requests.get(API_URL, params=PARAMS)
        response.raise_for_status()
        data = response.json()

        # Debugging: Print raw API response
        print("Raw API Response:", data)

        # Extract current weather data
        current_weather = data.get("current_weather", {})
        hourly = data.get("hourly", {})

        return {
            "temperature": current_weather.get("temperature", "N/A"),
            "humidity": hourly.get("humidity_2m", ["N/A"])[0] if "humidity_2m" in hourly else "N/A",
            "precipitation": hourly.get("precipitation", ["N/A"])[0] if "precipitation" in hourly else "N/A",
            "cloud_cover": hourly.get("cloudcover", ["N/A"])[0] if "cloudcover" in hourly else "N/A",
            "visibility": hourly.get("visibility", ["N/A"])[0] if "visibility" in hourly else "N/A",
            "uv_index": hourly.get("uv_index", ["N/A"])[0] if "uv_index" in hourly else "N/A",
            "pressure": hourly.get("pressure", ["N/A"])[0] if "pressure" in hourly else "N/A",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except requests.exceptions.RequestException as e:
        print(f"API Request failed: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}

def update_readme(data):
    """Updates the README.md file with IoT data."""
    dashboard = f"""
# IoT Dashboard

_Last Updated: {data.get('datetime', 'N/A')}_

## Current Weather Data:
- **Temperature:** {data.get('temperature', 'N/A')} °C
- **Humidity:** {data.get('humidity', 'N/A')} %
- **Precipitation:** {data.get('precipitation', 'N/A')} mm
- **Cloud Cover:** {data.get('cloud_cover', 'N/A')} %
- **Visibility:** {data.get('visibility', 'N/A')} km
- **UV Index:** {data.get('uv_index', 'N/A')}
- **Pressure:** {data.get('pressure', 'N/A')} hPa

*Powered by Open-Meteo API*

---

_Last Update Check: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_

"""
    with open("README.md", "w") as readme:
        readme.write(dashboard)
    print("README.md updated successfully.")

if __name__ == "__main__":
    iot_data = fetch_iot_data()
    if "error" in iot_data:
        print(iot_data["error"])
    update_readme(iot_data)
