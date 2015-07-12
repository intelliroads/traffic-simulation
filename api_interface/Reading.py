import json

class Reading(object):

    def __init__(self, sensor_id, speed, period, time):
        self.sensor_id = sensor_id
        self.speed = speed
        self.period = period
        self.time = time

    def toJSON(self):
        dic = {"sensorId":"{0}".format(self.sensor_id), "speed":self.speed, "period": self.period, "time":self.time}
        return json.dumps(dic)
