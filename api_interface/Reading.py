import json

class Reading(object):

	def __init__(self, sensor_id, speed, period):
		self.sensor_id = sensor_id
		self.speed = speed
		self.period = period

	def toJSON(self):
		dic = {"sensorId":"{0}".format(self.sensor_id), "speed":self.speed, "period": self.speed}
		return json.dumps(dic)


