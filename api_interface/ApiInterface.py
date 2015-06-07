import json
import requests
from api_interface.Reading import Reading

class ApiInterface(object):
    BASE_URL = "http://192.168.1.141:3000/"
    POST_READING = BASE_URL + "readings"
    
    #dummy 
    DETECTOR_DISTANCE = 1.5 

    @staticmethod
    def get(url):
        return requests.get(url).json()


    @staticmethod
    def post(url, payload):
        r = requests.post(url, data=payload)
        print r.text
        return r


    @staticmethod
    def post_reading(sensor_id, speed, period):
        return ApiInterface.post(ApiInterface.POST_READING, Reading(sensor_id, speed, period).toJSON())