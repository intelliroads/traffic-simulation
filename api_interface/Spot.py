from Road import Road
from RedLight import RedLight
from Toll import Toll
import unicodedata
class Spot(object):
    def __init__(self, spotJSON):
        self.id = spotJSON["_id"]
        self.type = spotJSON["type"]
        self.roads = []
        self.toll = None;
        self.red_light = None;
        for road in spotJSON["roads"]:
            self.roads.append(Road(road))
        if unicodedata.normalize('NFC', self.type) == unicodedata.normalize('NFC', u'trafficLight'):
            self.red_light = RedLight(spotJSON["redLight"])
        elif unicodedata.normalize('NFC', self.type) == unicodedata.normalize('NFC', u'toll'):
            self.toll = Toll(spotJSON["toll"])

    def __str__(self):
        return  "Spot - Id {0}, Type {1}, Roads {2}".format(self.id, self.type, self.roads)