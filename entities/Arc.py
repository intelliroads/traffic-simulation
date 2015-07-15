from enum import Enum


class ArcType(Enum):
    """
    Possible types of arcs:
        - uninterrupted: The arc represents an uninterrupted section of the road.
        - toll: The arc represents a toll in the road, in this case nodeA and nodeB are the start and finish of the toll.
        - traffic_light: The arc represents a traffic light in the road, in this case nodeA and nodeB are the start
          and finish of the toll.
    """
    uninterrupted = 1
    toll = 2
    traffic_light = 3


class Arc(object):
    """
    Graph arc
    """

    def __init__(self, arcType=None, nodeA=None, nodeB=None, cost=None, distance=None):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.cost = cost
        self.distance = distance
        self.type = arcType
