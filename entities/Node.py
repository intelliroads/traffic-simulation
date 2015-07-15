from enum import Enum

from entities.Arc import Arc


class NodeType(Enum):
    """
    Types of possible nodes
    """
    sensor = 1
    fork = 2
    toll = 3
    traffic_light = 4
    ordinary = 5
    finish = 6


class Node(object):
    """Generic graph node"""
    def __init__(self, nodeId, nodeType, roads, x, y):
        self.nodeType = nodeType
        self.nodeId = nodeId
        self.outArcs = []
        self.roads = roads
        self.x = x
        self.y = y

    def addArc(self, arcType, nodeB, cost, distance):
        """Add outer arc from current node to destination node"""
        self.outArcs.append(Arc(arcType, self, nodeB, cost, distance))

    def __repr__(self):
        return self.nodeId


class TollNode(Node):
    """Node that represents a toll in the road"""
    def __init__(self, nodeId, nodeType, servers, service_rate, road, x, y):
        super(TollNode, self).__init__(nodeId, nodeType, road, x, y)
        self.servers = servers
        self.service_rate = service_rate


class TrafficLightNode(Node):
    """Node that represents a traffic light in the road"""
    def __init__(self, nodeId, nodeType, duration, frequency, road, x, y):
        super(TrafficLightNode, self).__init__(nodeId, nodeType, road, x, y)
        self.duration = duration
        self.frequency = frequency