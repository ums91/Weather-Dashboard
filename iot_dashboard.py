import requests
import datetime

# IoT API configuration
API_URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": 34.1489,  # Replace with your location's latitude
    "longitude": 74.8377,  # Replace with your location's longitude
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
        if value >= 128:
            return "https://img.shields.io/badge/Wind%20Speed-Hurricane-red"
        elif value >= 112:
            return "https://img.shields.io/badge/Wind%20Speed-Storm-red"
        elif value >= 96:
            return "https://img.shields.io/badge/Wind%20Speed-Whole%20Gale-orange"
        elif value >= 80:
            return "https://img.shields.io/badge/Wind%20Speed-Strong%20Gale-orange"
        elif value >= 72:
            return "https://img.shields.io/badge/Wind%20Speed-Fresh%20Gale-orange"
        elif value >= 56:
            return "https://img.shields.io/badge/Wind%20Speed-Moderate%20Gale-yellow"
        elif value >= 48:
            return "https://img.shields.io/badge/Wind%20Speed-Strong%20Breeze-yellow"
        elif value >= 40:
            return "https://img.shields.io/badge/Wind%20Speed-Fresh%20Breeze-green"
        elif value >= 32:
            return "https://img.shields.io/badge/Wind%20Speed-Moderate%20Breeze-blue"
        elif value >= 26:
            return "https://img.shields.io/badge/Wind%20Speed-Gentle%20Breeze-blue"
        elif value >= 18:
            return "https://img.shields.io/badge/Wind%20Speed-Light%20Breeze-blue"
        else:
            return "https://img.shields.io/badge/Wind%20Speed-Light%20Wind-blue"

def update_readme(data):
    """Updates the README.md file with IoT data and badges."""
    temp_badge = get_badge_url(data.get("temperature"), "temperature")
    wind_badge = get_badge_url(data.get("windspeed"), "windspeed")

    dashboard = f"""
# Weather Dashboard

_Last Updated: {data.get('datetime', 'N/A')}_

## Current Weather Data: (Srinagar, JK)
- **Temperature:** {data.get('temperature', 'N/A')} °C ![Temperature Badge]({temp_badge})
- **Wind Speed:** {data.get('windspeed', 'N/A')} km/h ![Wind Speed Badge]({wind_badge})

*Powered by Open-Meteo API*
"""
    with open("README.md", "w") as readme:
        readme.write(dashboard)

if __name__ == "__main__":
    iot_data = fetch_iot_data()
    update_readme(iot_data)
