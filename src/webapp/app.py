import requests
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("welcome.html")


@app.route('/result', methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    date = output["date"]

    return render_template('welcome.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
