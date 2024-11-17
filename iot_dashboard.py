import requests
import datetime

# IoT API configuration (replace with actual API and endpoint)
API_URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": 18.5277,  # Replace with your location's latitude
    "longitude": 73.9515,  # Replace with your location's longitude
    "current_weather": True
}

def fetch_iot_data():
    """Fetches IoT data from the API."""
    try:
        response = requests.get(API_URL, params=PARAMS)
        response.raise_for_status()
        data = response.json()
        weather = data.get("current_weather", {})
        return {
            "temperature": weather.get("temperature"),
            "windspeed": weather.get("windspeed"),
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {"error": str(e)}

def get_badge_url(value, category):
    """Returns a badge URL with dynamic colors based on severity."""
    if value is None:
        return "https://img.shields.io/badge/Status-N/A-lightgrey"
    
    if category == "temperature":
        if value > 40:
            return "https://img.shields.io/badge/Temperature-Severe%20Temp-red"
        elif 30 < value <= 40:
            return "https://img.shields.io/badge/Temperature-High%20Temp-orange"
        elif 20 <= value <= 30:
            return "https://img.shields.io/badge/Temperature-Medium%20Temp-green"
        else:
            return "https://img.shields.io/badge/Temperature-Low%20Temp-blue"
    
    if category == "windspeed":
        if value > 40:
            return "https://img.shields.io/badge/Wind%20Speed-Severe%20Wind-red"
        elif 30 < value <= 40:
            return "https://img.shields.io/badge/Wind%20Speed-High%20Wind-orange"
        elif 20 <= value <= 30:
            return "https://img.shields.io/badge/Wind%20Speed-Medium%20Wind-green"
        else:
            return "https://img.shields.io/badge/Wind%20Speed-Low%20Wind-blue"

def update_readme(data):
    """Updates the README.md file with IoT data and badges."""
    temp_badge = get_badge_url(data.get("temperature"), "temperature")
    wind_badge = get_badge_url(data.get("windspeed"), "windspeed")

    dashboard = f"""
# Weather Dashboard

_Last Updated: {data.get('datetime', 'N/A')}_

## Current Weather Data: (Pune, MH)
- **Temperature:** {data.get('temperature', 'N/A')} °C ![Temperature Badge]({temp_badge})
- **Wind Speed:** {data.get('windspeed', 'N/A')} km/h ![Wind Speed Badge]({wind_badge})

*Powered by Open-Meteo API*
"""
    with open("README.md", "w") as readme:
        readme.write(dashboard)

if __name__ == "__main__":
    iot_data = fetch_iot_data()
    update_readme(iot_data)
