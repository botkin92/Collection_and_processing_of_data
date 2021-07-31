import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("api_key", None)


def weather_data(city):
    url = 'https://api.openweathermap.org/data/2.5/weather'
    req = requests.get(f'{url}?q={city},uk&appid={api_key}')
    data = json.loads(req.text)
    return data


input_city = input("Enter the name of the city: ")
data = weather_data(input_city)
print(f"In {data['name']} {round(data['main']['temp'] - 273)} degrees Celsius")
