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

def get_temp_label(temp):
    """Returns the temperature label based on the value."""
    if temp is None:
        return "N/A"
    if temp > 40:
        return "Severe_Temp"
    elif 30 < temp <= 40:
        return "High_Temp"
    elif 20 <= temp <= 30:
        return "Medium_Temp"
    else:
        return "Low_Temp"

def get_wind_label(speed):
    """Returns the wind speed label based on the value."""
    if speed is None:
        return "N/A"
    if speed > 150:
        return "Severe_Wind"
    elif 80 < speed <= 150:
        return "High_Wind"
    elif 30 <= speed <= 80:
        return "Medium_Wind"
    else:
        return "Low_Wind"

def update_readme(data):
    """Updates the README.md file with IoT data."""
    temp_label = get_temp_label(data.get("temperature"))
    wind_label = get_wind_label(data.get("windspeed"))

    dashboard = f"""
# Current Weather Dashboard

_Last Updated: {data.get('datetime', 'N/A')}_

## Current Weather Data: (Pune, MH)
- **Temperature:** {data.get('temperature', 'N/A')} °C ({temp_label})
- **Wind Speed:** {data.get('windspeed', 'N/A')} km/h ({wind_label})

*Powered by Open-Meteo API*
"""
    with open("README.md", "w") as readme:
        readme.write(dashboard)

if __name__ == "__main__":
    iot_data = fetch_iot_data()
    update_readme(iot_data)
