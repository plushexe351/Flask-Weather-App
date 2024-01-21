from flask import Flask, render_template, request
from weather import get_current_weather, fahrenheit_to_celsius
from waitress import serve

app = Flask(__name__)

SAMPLE_CITY_1 = "New Delhi"
SAMPLE_CITY_2 = "California"

def get_weather_data(city):
    if not bool(city.strip()):
        city = SAMPLE_CITY_1

    return get_current_weather(city)

@app.route('/')
@app.route('/index')
def index():
    weather_data1 = get_weather_data(SAMPLE_CITY_1)
    weather_data2 = get_weather_data(SAMPLE_CITY_2)

    return render_template(
        "index.html",
        temp1="{:.1f}".format(fahrenheit_to_celsius(float(weather_data1['main']['temp']))),
        temp2="{:.1f}".format(fahrenheit_to_celsius(float(weather_data2['main']['temp'])))
    )

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    weather_data1 = get_weather_data(SAMPLE_CITY_1)
    weather_data2 = get_weather_data(SAMPLE_CITY_2)

    weather_data = get_weather_data(city)

    if not weather_data['cod'] == 200:
        return render_template(
        "city_not_found.html",
        temp1="{:.1f}".format(fahrenheit_to_celsius(float(weather_data1['main']['temp']))),
        temp2="{:.1f}".format(fahrenheit_to_celsius(float(weather_data2['main']['temp'])))
        )

    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp="{:.1f}".format(fahrenheit_to_celsius(float(weather_data['main']['temp']))),
        feels_like="{:.1f}".format(fahrenheit_to_celsius(float(weather_data['main']['feels_like']))),
        temp1="{:.1f}".format(fahrenheit_to_celsius(float(weather_data1['main']['temp']))),
        temp2="{:.1f}".format(fahrenheit_to_celsius(float(weather_data2['main']['temp'])))
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port="3000")
