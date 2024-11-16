import requests
import datetime

# IoT API configuration (replace with actual API and endpoint)
API_URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    #"latitude": 18.5277,  # Replace with your location's latitude 
    #"longitude": 73.9515,  # Replace with your location's longitude
    "latitude": 34.1481,  # Replace with your location's latitude 
    "longitude": 74.8418,  # Replace with your location's longitude
    
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

def update_readme(data):
    """Updates the README.md file with IoT data."""
    dashboard = f"""
# Weather Dashboard for Pune, MH

_Last Updated: {data.get('datetime', 'N/A')}_

## Current Weather Data:
- **Temperature:** {data.get('temperature', 'N/A')} °C
- **Wind Speed:** {data.get('windspeed', 'N/A')} km/h

*Powered by Open-Meteo API*
"""
    with open("README.md", "w") as readme:
        readme.write(dashboard)

if __name__ == "__main__":
    iot_data = fetch_iot_data()
    update_readme(iot_data)
