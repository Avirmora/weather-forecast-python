import requests
from datetime import datetime


def get_weather(city_name, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'imperial'  # 'imperial' for Fahrenheit
    }

    response = requests.get(url, params=params).json()
    if not response or response.get('cod') != 200:
        return {'error': 'Failed to retrieve weather data.'}
    
    return {
        'city': response['name'],
        'temperature': round(response['main']['temp']),
        'feels_like': round(response['main']['feels_like']),
        'description': response['weather'][0]['description'].title(),
        'humidity': response['main']['humidity'],
        'wind_speed': response['wind']['speed'],
        'pressure': response['main']['pressure'],
        'visibility': response.get('visibility', 10000) / 1000,  # in km
    }


def get_5_day_forecast(city_name, api_key):
    url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(url, params=params).json()
    if 'list' not in response:
        return {'error': 'No forecast data available.'}

    forecast_by_day = {}
    for entry in response['list']:
        date = datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d')
        if date not in forecast_by_day:
            forecast_by_day[date] = {'temps': [], 'conditions': []}
        forecast_by_day[date]['temps'].append(entry['main']['temp'])
        forecast_by_day[date]['conditions'].append(entry['weather'][0]['description'].title())

    forecast_summary = []
    for date, info in forecast_by_day.items():
        min_temp = round(min(info['temps']))
        max_temp = round(max(info['temps']))
        common_condition = max(set(info['conditions']), key=info['conditions'].count)
        forecast_summary.append(f"{date}: {common_condition}, {min_temp}°C - {max_temp}°C")

    return forecast_summary[:5]  # Return 5-day summary


def get_weather_theme(description, city):
    desc = description.lower()
    
    if any(keyword in desc for keyword in ['sun', 'clear']):
        # ☀️ Sunny
        return f"\033[1;41;93m   ☀️  WEATHER IN {city.upper()}   \033[0m"

    elif any(keyword in desc for keyword in ['rain', 'drizzle', 'showers']):
        # 🌧 Rainy
        return f"\033[1;44;97m   🌧 WEATHER IN {city.upper()}   \033[0m"

    elif 'snow' in desc:
        # 🌨 Snow
        return f"\033[1;107;94m   🌨 WEATHER IN {city.upper()}   \033[0m"

    elif any(keyword in desc for keyword in ['cloud', 'overcast', 'mist', 'fog']):
        # ☁️ Cloudy
        return f"\033[1;47;30m   ☁️ WEATHER IN {city.upper()}   \033[0m"

    elif any(keyword in desc for keyword in ['storm', 'thunder']):
        # ⛈️ Thunderstorm
        return f"\033[1;45;93m   ⛈️  WEATHER IN {city.upper()}   \033[0m"

    else:
        # Default
        return f"\033[1;40;96m   🌤️  WEATHER IN {city.upper()}   \033[0m"

#city name
city = input("Enter city name: ").title()
#api key from https://home.openweathermap.org/api_keys 
api_key = "88a2446dd6ce0c50f52fdcd109e1f726"

weather_data = get_weather(city, api_key)

if 'error' in weather_data:
    print("Error:", weather_data['error'])
else:
    theme_header = get_weather_theme(weather_data['description'], weather_data['city'])
    print(f"\n{theme_header}\n")
    print(f"Temperature Fahrenheit: {weather_data['temperature']}°F (Feels like {weather_data['feels_like']}°F)")
    print(f"Temperature Celsius: {round((weather_data['temperature'] - 32) * 5 / 9)}°C "
          f"(Feels like {round((weather_data['feels_like'] - 32) * 5 / 9)}°C)")    
    print(f"Condition: {weather_data['description']}")
    print(f"Humidity: {weather_data['humidity']}%")
    print(f"Wind Speed: {weather_data['wind_speed']} m/s")
    print(f"Pressure: {weather_data['pressure']} hPa")
    print(f"Visibility: {weather_data['visibility']} km")

    print("\n5-Day Forecast:")
    forecast = get_5_day_forecast(city, api_key)
    if isinstance(forecast, dict) and 'error' in forecast:
        print("Forecast error:", forecast['error'])
    else:
        for day in forecast:
            print(" ", day)