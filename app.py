
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Enter your actual OpenWeatherMap API key here
API_KEY = "e3d3e8c300ebf1bc9cf0ca2930089f51"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/weather", methods=["POST"])
def weather():

    city = request.form.get("city", "").strip()

    if not city:
        return render_template(
            "index.html",
            error="Please enter a city name!"
        )

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if response.status_code != 200:
            if response.status_code == 401:
                error = "Invalid API key! Please check your API key."
            elif response.status_code == 404:
                error = "City not found! Please try again."
            else:
                error = "Weather service error. Please try again."

            return render_template("index.html", error=error)

        temperature = data["main"]["temp"]
        condition = data["weather"][0]["main"]

        if condition in ["Rain", "Drizzle", "Thunderstorm"]:
            weather_type = "rainy"
            message = "Take your umbrella! Stay dry! 💗"

        elif temperature >= 30:
            weather_type = "hot"
            message = "It's a hot day! Stay hydrated! ☀️"

        elif temperature <= 15:
            weather_type = "cold"
            message = "Brrr! It's cold! Stay warm! ❄️"

        else:
            weather_type = "pleasant"
            message = "Enjoy this beautiful weather! 🌈"

        weather_data = {
            "city": data["name"],
            "temperature": temperature,
            "condition": data["weather"][0]["description"].title(),
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "feels": data["main"]["feels_like"],
            "weather_type": weather_type,
            "message": message
        }

        return render_template(
            "weather.html",
            weather=weather_data
        )

    except requests.exceptions.RequestException:
        return render_template(
            "index.html",
            error="Internet connection problem. Try again!"
        )


if __name__ == "__main__":
    app.run(debug=True)
