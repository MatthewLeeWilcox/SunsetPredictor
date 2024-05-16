import requests
from flask import Flask, render_template, request

from helpers.future_weather_api import get_future_weather
from helpers.mock_output import genSunsetImage

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("welcome.html")


@app.route('/result', methods=['POST', 'GET']) 
def result():
    if request.method == 'POST':
        output = request.form.to_dict()
        date = output["date"]
        try:
            df_weather = get_future_weather(date)
            genSunsetImage(df_weather)
            return render_template('result.html', data=df_weather.to_html())
        
        except Exception as e:
            return render_template('Error.html')

    else:

        return render_template('welcome.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
