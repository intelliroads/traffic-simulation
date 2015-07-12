import json
import requests
from api_interface.Reading import Reading
from api_interface.Spot import Spot
from api_interface.Sensor import Sensor
import time

current_milli_time = lambda: int(round(time.time() * 1000))

class ApiInterface(object):
    BASE_URL = "http://127.0.0.1:3000/"
    READING = BASE_URL + "readings"
    SPOTS = BASE_URL + "spots"
    SENSORS = BASE_URL + "sensors"
    SPEED = BASE_URL + "roads/{0}/mean-time-speed"
    VOLUME = BASE_URL + "roads/{0}/volume"

    @staticmethod
    def get(url, payload):
        if payload != None:
            return requests.get(url, params=payload).json()
        else:
            return requests.get(url).json()


    @staticmethod
    def post(url, payload):
        return requests.post(url, data=payload)


    @staticmethod
    def post_reading(sensor_id, speed, period, time):
        return ApiInterface.post(ApiInterface.READING, Reading(sensor_id, speed, period, time).toJSON())

    @staticmethod
    def get_all_spots():
        spots = []
        response = ApiInterface.get(ApiInterface.SPOTS, None)
        for spotJson in response:
            spots.append(Spot(spotJson))
        return spots

    @staticmethod
    def get_all_sensors():
        sensors = []
        response = ApiInterface.get(ApiInterface.SENSORS, None)
        for sensorJson in response:
            sensors.append(Sensor(sensorJson))
        return sensors

    @staticmethod
    def get_speed(road_id, from_km, to_km, from_time, to_time):
        payload = {'fromKm': from_km, 'toKm': to_km, 'fromTime': from_time, 'toTime': to_time}
        return  ApiInterface.get(ApiInterface.SPEED.format(road_id), payload)


    @staticmethod
    def get_volume(road_id, km, from_time, to_time):
        payload = {'km': km, 'fromTime': from_time, 'toTime': to_time}
        return ApiInterface.get(ApiInterface.VOLUME.format(road_id), payload)
