import requests
from flask import Flask, render_template, request

from helpers.future_weather_api import get_future_weather


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("welcome.html")


@app.route('/result', methods=['POST', 'GET']) 
def result():
    if request.method == 'POST':
        output = request.form.to_dict()
        date = output["date"]
        if date == "05/15/2024":
            try:
                df_weather = get_future_weather(date)

                return render_template('result.html', data=df_weather.to_html())
            
            except Exception as e:
                return str(e), 500
        else:
            df_weather = get_future_weather(date)

            return render_template('resultRickRoll.html', data=df_weather.to_html())

    else:

        return render_template('welcome.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
