class Sensor(object):
    """
    Sensor located in one road provided by the api
    """

    def __init__(self, sensorJSON):
        self.id = sensorJSON["_id"]
        self.road_id = sensorJSON["roadId"]
        self.kilometer = sensorJSON["kilometer"]

    def __str__(self):
        return "Sensor - Id {0}, Road Id {1}, Km {2}".format(self.id, self.road_id, self.kilometer)

