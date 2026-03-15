from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

def get_next_quarter_dates():
    today = datetime.utcnow()
    end_date = today + timedelta(days=90)

    start = today.strftime("%Y-%m-%d")
    end = end_date.strftime("%Y-%m-%d")

    return start, end


def get_holidays():
    start, end = get_next_quarter_dates()

    url = "https://www.hebcal.com/hebcal"

    params = {
        "v": "1",
        "cfg": "json",
        "maj": "on",
        "start": start,
        "end": end
    }

    response = requests.get(url, params=params)
    data = response.json()

    holidays = []

    for item in data.get("items", []):
        holidays.append({
            "name": item.get("title"),
            "date": item.get("date")
        })

    return holidays


@app.route("/holidays", methods=["GET"])
def holidays():
    data = get_holidays()
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
