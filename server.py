from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
import requests
import json
import os

app = Flask(__name__)
load_dotenv()
CORS(app)

open_weather_url = 'https://api.openweathermap.org/data/2.5/forecast'
giphy_url = 'https://api.giphy.com/v1/gifs/random'
darksky_url = 'https://api.darksky.net/forecast'

@app.route("/")
def main():
  return "Hello world!"

@app.route("/api/forecast", methods=['GET'])
def get_forecast():
  lat = request.args.get('lat')
  lng = request.args.get('lng')
  response = requests.get(f'{darksky_url}/{os.getenv("DARK_SKY_API_KEY")}/{lat},{lng}', params={
    # 'lang': 'pl',
    'units': 'si'
  })
  return response.text
# def get_forecast():
#   response = requests.get(open_weather_url, params={
#     'appid': os.getenv('OPEN_WEATHER_MAP_API_KEY'),
#     'units': 'metric',
#     'lat': request.args.get('lat'),
#     'lon': request.args.get('lng'),
#     'cnt': request.args.get('days'),
#   })
#   return response.text

@app.route("/api/gif", methods=['GET'])
def get_gif():
  response = requests.get(giphy_url, params={
    'api_key': os.getenv('GIPHY_API_KEY'),
    'rating': 'G',
    'tag': request.args.get('tag')
  })
  return response.text


if __name__ == "__main__":
  app.run(host= '0.0.0.0')