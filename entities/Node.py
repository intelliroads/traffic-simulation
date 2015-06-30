from enum import Enum

from entities.Arc import Arc


class NodeType(Enum):
    sensor = 1
    fork = 2
    toll = 3
    traffic_light = 4
    ordinary = 5
    finish = 6


class Node(object):
    def __init__(self, nodeId, nodeType, route, kilometer):
        self.nodeType = nodeType
        self.nodeId = nodeId
        self.outArcs = []
        self.route = route
        self.kilometer = kilometer

    def addArc(self, arcType, nodeB, cost, distance):
        #Add outer arc from current node to destination node
        self.outArcs.append(Arc(arcType, self, nodeB, cost, distance))

    def __repr__(self):
        return self.nodeId


class TollNode(Node):
    def __init__(self, nodeId, nodeType, servers, service_rate, route, kilometer):
        super(TollNode, self).__init__(nodeId, nodeType, route, kilometer)
        self.servers = servers
        self.service_rate = service_rate


class TrafficLightNode(Node):
    def __init__(self, nodeId, nodeType, duration, frequency, route,kilometer):
        super(TrafficLightNode, self).__init__(nodeId, nodeType,route, kilometer)
        self.duration = duration
        self.frequency = frequency
