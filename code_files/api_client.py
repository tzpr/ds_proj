
import requests # http://docs.python-requests.org/en/master/
import json     # https://docs.python.org/3/library/json.html



PREDICT_API_URL = 'http://127.0.0.1:5000/predict'
HELLO_API_URL   = 'http://127.0.0.1:5000/hello'

CONSUMPTION_FILE = '../data/energy_industrial.csv'
WEATHER_FILE = '../data/hourly_resampled_weather_data.csv'


# construct a payload for the prediction POST request
# POST contains two files: consumption data and weather data
#forecast_base_data = [('files', open(CONSUMPTION_FILE, 'rb')), ('files', open(WEATHER_FILE, 'rb'))]

# make the POST 
# TODO: this fails... payload too big?
#response = requests.post(PREDICT_API_URL, files=forecast_base_data)

# GET request for a sanity check
response = requests.get(HELLO_API_URL)

# server response
print('Response from server:', response.text)