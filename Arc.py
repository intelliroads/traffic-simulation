from enum import Enum


class ArcType(Enum):
    uninterrupted = 1
    toll = 2
    traffic_light = 3

class Arc(object):
    def __init__(self, arcType, nodeA, nodeB, cost, distance):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.cost = cost
        self.distance = distance
        self.type = arcType


