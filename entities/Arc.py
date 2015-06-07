from enum import Enum


class ArcType(Enum):
    uninterrupted = 1
    toll = 2
    traffic_light = 3

class Arc(object):
    def __init__(self, arcType = None, nodeA=None, nodeB=None, cost=None, distance=None):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.cost = cost
        self.distance = distance
        self.type = arcType
