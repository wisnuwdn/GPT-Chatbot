from flask import Flask, request
import requests

app = Flask(__name__)


@app.route("/weather")
async def home():
    api_key = "" #insert API key
    city = request.args.get('city', 'Paris')
    country = request.args.get('country', 'fr')
    print('city', city)
    print('country', country)
    result = requests.get(
        "http://api.openweathermap.org/data/2.5/weather",
        params={
            "q": f"{city}, {country}",
            "APPID": api_key
        })

    res = result.json()
    print(res)
    return {"result": res}


if __name__ == "__main__":
    app.run(debug=True)
