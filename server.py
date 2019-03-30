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

INDEX = 2
DATABASE = [{
  "id": 0,
  "name": "Tomek",
  "url": "https://svr21.supla.org/direct/67/WzYZzmZMzEY2Y5gG/read"
}, {
  "id": 1,
  "name": "Szymon",
  "url": "https://svr21.supla.org/direct/67/WzYZzmZMzEY2Y5gG/read"
}, {
  "id": 2,
  "name": "Tomek",
  "url": "https://svr21.supla.org/direct/67/WzYZzmZMzEY2Y5gG/read"
}]

@app.route("/")
def main():
  return "Hello world!"

@app.route("/api/sensors", methods=['GET'])
def get_sensors():
  SENSORS = []
  for sensor in DATABASE:
    response = requests.get(sensor["url"])
    SENSORS.append({
      "id": sensor["id"],
      "name": sensor["name"],
      "measurement": response.json(),
    })
  return jsonify(SENSORS)

@app.route("/api/sensors", methods=['POST'])
def add_sensors():
  global INDEX
  INDEX = INDEX +1
  content = request.get_json()
  DATABASE.append({
    "id": INDEX,
    **content,
  })
  return jsonify(DATABASE)
 
@app.route("/api/sensors/<int:sensor_id>", methods=['DELETE'])
def remove_sensor(sensor_id):
  global DATABASE
  DATABASE = [sensor for sensor in DATABASE if not (sensor['id'] == sensor_id)] 
  return jsonify(DATABASE)

@app.route("/api/forecast", methods=['GET'])
def get_forecast():
  lat = request.args.get('lat')
  lng = request.args.get('lng')
  response = requests.get(f'{darksky_url}/{os.getenv("DARK_SKY_API_KEY")}/{lat},{lng}', params={
    'lang': 'pl',
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