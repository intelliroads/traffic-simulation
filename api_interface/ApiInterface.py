import json
import requests
from api_interface.Reading import Reading

class ApiInterface(object):
    BASE_URL = "http://localhost:3000/"
    POST_READING = BASE_URL + "readings"


    @staticmethod
    def get(url):
        return requests.get(url).json()


    @staticmethod
    def post(url, payload):
        return requests.post(url, data=payload)


    @staticmethod
    def post_reading(sensor_id, speed, period):
        return ApiInterface.post(ApiInterface.POST_READING, Reading(sensor_id, speed, period).toJSON())
