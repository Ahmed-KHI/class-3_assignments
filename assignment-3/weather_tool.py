import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)
weather_api_key = os.getenv("WEATHER_API_KEY")

def get_weather(city: str) -> str:
    """
    Fetch weather information for a given city using WeatherAPI.
    Returns temperature and weather condition for the city.
    """
    try:
        url = f"http://api.weatherapi.com/v1/current.json"
        params = {
            'key': weather_api_key,
            'q': city,
            'aqi': 'no'  
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()  
        
        data = response.json()
        
        location = data['location']['name']
        country = data['location']['country']
        temperature_c = data['current']['temp_c']
        temperature_f = data['current']['temp_f']
        condition = data['current']['condition']['text']
        humidity = data['current']['humidity']
        feels_like_c = data['current']['feelslike_c']
        
        weather_info = f"""
Weather in {location}, {country}:
🌡️ Temperature: {temperature_c}°C ({temperature_f}°F)
🌤️ Condition: {condition}
🤚 Feels like: {feels_like_c}°C
💧 Humidity: {humidity}%
        """.strip()
        
        return weather_info
        
    except requests.RequestException as e:
        return f"❌ Error fetching weather data: {str(e)}"
    except KeyError as e:
        return f"❌ Error parsing weather data: Missing key {str(e)}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

if __name__ == "__main__":
    test_city = "Karachi"
    result = get_weather(test_city)
    print(f"Testing weather for {test_city}:")
    print(result)
