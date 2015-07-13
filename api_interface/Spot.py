from api_interface.Road import Road
from api_interface.RedLight import RedLight
from api_interface.Toll import Toll
import unicodedata

class Spot(object):
    def __init__(self, spotJSON):
        self.id = spotJSON["_id"]
        self.type = spotJSON["type"]
        self.roads = []
        self.location = spotJSON["location"]
        self.toll = None;
        self.red_light = None;
        for road in spotJSON["roads"]:
            self.roads.append(Road(road))
        if unicodedata.normalize('NFC', self.type) == unicodedata.normalize('NFC', u'trafficLight'):
            self.red_light = RedLight(spotJSON["redLight"])
        elif unicodedata.normalize('NFC', self.type) == unicodedata.normalize('NFC', u'toll'):
            self.toll = Toll(spotJSON["toll"])

    def get_kilometer_of_route(self, road_id):
        for road in self.roads:
            if road.id == road_id:
                return road.kilometer

    def __str__(self):
        return  "Spot - Id {0}, Type {1}, Roads {2}".format(self.id, self.type, self.roads)