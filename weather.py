from dotenv import load_dotenv
from pprint import pprint
import requests
import os

load_dotenv()

def get_current_weather(city="New Delhi"):
    api_key = os.getenv("API_KEY")
    request_url = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city}&units=imperial"
    print(request_url)

    weather_data = requests.get(request_url).json()

    return weather_data

def fahrenheit_to_celsius(fahrenheit):
    celsius = (fahrenheit - 32) * 5 / 9
    return celsius

if __name__ == "__main__":
    print('\n Get Current Weather Conditions \n')

    city = input("\nPlease enter a city name: ")

    weather_data = get_current_weather(city)

    print("\n")
    pprint(weather_data)
  