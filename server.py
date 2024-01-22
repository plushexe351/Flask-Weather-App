from flask import Flask, render_template, request
from weather import get_current_weather, fahrenheit_to_celsius
from waitress import serve
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder

app = Flask(__name__)

SAMPLE_CITY_1 = "New Delhi"
SAMPLE_CITY_2 = "California"
SAMPLE_CITY_3 = "Tokyo"
SAMPLE_CITY_4 = "Siliguri"

def get_weather_data(city):
    if not bool(city.strip()):
        city = SAMPLE_CITY_1

    return get_current_weather(city)

@app.route('/')
@app.route('/index')
def index():
    weather_data1 = get_weather_data(SAMPLE_CITY_1)
    weather_data2 = get_weather_data(SAMPLE_CITY_2)
    weather_data3 = get_weather_data(SAMPLE_CITY_3)
    weather_data4 = get_weather_data(SAMPLE_CITY_4)

    return render_template(
        "index.html",
        temp1="{:.1f}".format(fahrenheit_to_celsius(float(weather_data1['main']['temp']))),
        temp2="{:.1f}".format(fahrenheit_to_celsius(float(weather_data2['main']['temp']))),
        temp3="{:.1f}".format(fahrenheit_to_celsius(float(weather_data3['main']['temp']))),
        temp4="{:.1f}".format(fahrenheit_to_celsius(float(weather_data4['main']['temp'])))
    )

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    weather_data1 = get_weather_data(SAMPLE_CITY_1)
    weather_data2 = get_weather_data(SAMPLE_CITY_2)
    weather_data3 = get_weather_data(SAMPLE_CITY_3)
    weather_data4 = get_weather_data(SAMPLE_CITY_4)

    weather_data = get_weather_data(city)

    if not weather_data['cod'] == 200:
        return render_template(
        "city_not_found.html",
        temp1="{:.1f}".format(fahrenheit_to_celsius(float(weather_data1['main']['temp']))),
        temp2="{:.1f}".format(fahrenheit_to_celsius(float(weather_data2['main']['temp']))),
        temp3="{:.1f}".format(fahrenheit_to_celsius(float(weather_data3['main']['temp']))),
        temp4="{:.1f}".format(fahrenheit_to_celsius(float(weather_data4['main']['temp'])))
        )

    timestamp = weather_data['dt']

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
        temp1="{:.1f}".format(fahrenheit_to_celsius(float(weather_data1['main']['temp']))),
        max_temp="{:.1f}".format(fahrenheit_to_celsius(float(weather_data['main']['temp_max']))),
        min_temp="{:.1f}".format(fahrenheit_to_celsius(float(weather_data['main']['temp_min']))),
        humidity=weather_data['main']['humidity'],
        pressure=weather_data['main']['pressure'],
        country_code=weather_data['sys']['country'],
        temp2="{:.1f}".format(fahrenheit_to_celsius(float(weather_data2['main']['temp']))),
         temp3="{:.1f}".format(fahrenheit_to_celsius(float(weather_data3['main']['temp']))),
        temp4="{:.1f}".format(fahrenheit_to_celsius(float(weather_data4['main']['temp']))),
        time = formatted_time
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port="3000")
