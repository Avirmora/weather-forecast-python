import requests

def get_weather(city_name, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'imperial'  # Use 'imperial' for Fahrenheit
    }

    #print("Requesting:", base_url, "with params:", params)  # Debug line
    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            return {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
            #return weather
        else:
            return {'error': f"{data.get('message', 'Unknown error')} (code: {response.status_code})"}
            #return {'error': data.get('message', 'Failed to get weather')}
    except Exception as e:
        return {'error': str(e)}
# Example usage
city = input("Enter city name: ").title()
api_key = "88a2446dd6ce0c50f52fdcd109e1f726"  # Replace with your API key

weather_data = get_weather(city, api_key)

if 'error' in weather_data:
    print("Error:", weather_data['error'])
else:
    print(f"Weather in {weather_data['city']}:")
    print(f"Temperature Fahrenheit: {weather_data['temperature']}°F")
    print(f"Temperature Celsius: {round((weather_data['temperature'] - 32) * 5/9)}°C")
    print(f"Condition: {weather_data['description']}")
    print(f"Humidity: {weather_data['humidity']}%")
    print(f"Wind Speed: {weather_data['wind_speed']} m/s")