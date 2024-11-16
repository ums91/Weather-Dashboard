import requests
import datetime
import os

# IoT API configuration (replace with actual API and endpoint)
API_URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": 40.7128,  # Replace with your location's latitude
    "longitude": -74.0060,  # Replace with your location's longitude
    "current_weather": True,
    "hourly": "temperature_2m,humidity_2m,precipitation,cloudcover,visibility,uv_index,pressure"
}

def fetch_iot_data():
    """Fetches IoT data from the API."""
    try:
        response = requests.get(API_URL, params=PARAMS)
        response.raise_for_status()
        data = response.json()
        current_weather = data.get("current_weather", {})
        hourly = data.get("hourly", {})
        
        # Extracting required values
        temperature = current_weather.get("temperature", "N/A")
        humidity = hourly.get("humidity_2m", ["N/A"])[0]
        precipitation = hourly.get("precipitation", ["N/A"])[0]
        cloud_cover = hourly.get("cloudcover", ["N/A"])[0]
        visibility = hourly.get("visibility", ["N/A"])[0]
        uv_index = hourly.get("uv_index", ["N/A"])[0]
        pressure = hourly.get("pressure", ["N/A"])[0]

        return {
            "temperature": temperature,
            "humidity": humidity,
            "precipitation": precipitation,
            "cloud_cover": cloud_cover,
            "visibility": visibility,
            "uv_index": uv_index,
            "pressure": pressure,
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {"error": str(e)}

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
    
    # Force an update to README (timestamp change)
    readme_file_path = "README.md"
    with open(readme_file_path, "w") as readme:
        readme.write(dashboard)
    return True  # File is updated

if __name__ == "__main__":
    iot_data = fetch_iot_data()
    update_readme(iot_data)
