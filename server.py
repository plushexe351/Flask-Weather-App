from flask import Flask, render_template, request
from weather import get_current_weather, fahrenheit_to_celsius
from waitress import serve
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz

app = Flask(__name__)

SAMPLE_CITIES = ["New Delhi","California","Tokyo","Siliguri"]


def get_weather_data(city):
    if not bool(city.strip()):
        city = SAMPLE_CITY_1

    return get_current_weather(city)

def format_temperature(weather_data):
    return "{:.1f}".format(fahrenheit_to_celsius(float(weather_data['main']['temp'])))

@app.route('/')
@app.route('/index')
def index():
 
    # loading sample locations data 
      
    sampleCityWeatherData = [get_weather_data(city) for city in SAMPLE_CITIES]
    temperatures = [format_temperature(data) for data in sampleCityWeatherData]

    return render_template(
        "index.html",
        temp1=temperatures[0],
        temp2=temperatures[1],
        temp3=temperatures[2],
        temp4=temperatures[3]
    )

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    
    sampleCityWeatherData = [get_weather_data(city) for city in SAMPLE_CITIES]
    temperatures = [format_temperature(data) for data in sampleCityWeatherData]
    
    weather_data = get_weather_data(city)

    if not weather_data['cod'] == 200:
        return render_template(
        "city_not_found.html",
        temp1=temperatures[0],
        temp2=temperatures[1],
        temp3=temperatures[2],
        temp4=temperatures[3]
        )

    timestamp = weather_data['dt']
    sunriset_timestamp = weather_data['sys']['sunrise']
    sunset_timestamp = weather_data['sys']['sunset']

    # Convert the timestamp to a datetime object in UTC
    date_object_utc = datetime.utcfromtimestamp(timestamp)

    # Use timezonefinder to get the timezone based on the city's coordinates
    latitude, longitude = weather_data['coord']['lat'], weather_data['coord']['lon']
    tf = TimezoneFinder()
    city_timezone_str = tf.timezone_at(lat=latitude, lng=longitude)

    # Convert UTC time to the local time of the city
    city_timezone = pytz.timezone(city_timezone_str)
    date_object_localized = date_object_utc.replace(tzinfo=pytz.utc).astimezone(city_timezone)

    # Extract the time portion from the localized datetime object
    formatted_time = date_object_localized.strftime('%H:%M')

    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp="{:.1f}".format(fahrenheit_to_celsius(float(weather_data['main']['temp']))),
        feels_like="{:.1f}".format(fahrenheit_to_celsius(float(weather_data['main']['feels_like']))),
        max_temp="{:.1f}".format(fahrenheit_to_celsius(float(weather_data['main']['temp_max']))),
        min_temp="{:.1f}".format(fahrenheit_to_celsius(float(weather_data['main']['temp_min']))),
        temp1=temperatures[0],
        temp2=temperatures[1],
        temp3=temperatures[2],
        temp4=temperatures[3],
        humidity=weather_data['main']['humidity'],
        pressure=weather_data['main']['pressure'],
        country_code=weather_data['sys']['country'],
        time = formatted_time
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port="3000")
