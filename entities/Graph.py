from entities.Arc import ArcType
from api_interface.ApiInterface import ApiInterface
from api_interface.Spot import Spot
from entities.Node import Node, TollNode, TrafficLightNode, NodeType
from costs.CostCalculator import CostCalculator
import unicodedata
import copy

class Graph(object):
    def __init__(self, env, recalculationStep):
        self.env = env
        self.recalculationStep = recalculationStep
        spots = ApiInterface.get_all_spots()
        sensors = ApiInterface.get_all_sensors()
        self.nodes = []
        self.initNodes(spots,sensors)

    def initNodes(self, spots, sensors):
        dict = {}
        # Creation of dictionary to store spots_list of sensors and spots by roadId
        for spot in spots:
            for road in spot.roads:
                auxSpot = copy.copy(spot)
                auxSpot.roads = [road]
                if(not dict.has_key(road.id)):
                    dict[road.id] = []
                dict[road.id].append(auxSpot)
        for sensor in sensors:
            if not dict.has_key(sensor.road_id):
                dict[sensor.road_id] = []
            dict[sensor.road_id].append(sensor)
        # Order sub lists by kilometer
        for key in dict.keys():
            dict[key].sort(key = lambda x: x.roads[0].kilometer if isinstance(x,Spot) else x.kilometer,
                                       reverse = False)

        # Transform dictionary into Nodes and Arcs
        forkNodes = []
        nodes = []
        for key in dict.keys():
            spots_list = dict[key]
            last_node = None
            for element in spots_list:
                node = None
                if isinstance(element, Spot):
                    if unicodedata.normalize('NFC', element.type) == unicodedata.normalize('NFC', u'fork'):
                        node = next((x for x in forkNodes if x.nodeId == element.id),None)
                        if node == None:
                            location = element.location.split(',')
                            node = Node(element.id, NodeType.fork, element.roads[0].id ,element.roads[0].kilometer, location[0], location[1])
                            nodes.append(node)
                            forkNodes.append(node)
                    elif unicodedata.normalize('NFC', element.type) == unicodedata.normalize('NFC', u'toll'):
                        #If the node is interrupted we need the start and end of itself
                        location = element.location.split(',')
                        node = TollNode(element.id, NodeType.toll, element.toll.number_of_servers, element.toll.service_rate,element.roads[0].id ,element.roads[0].kilometer, location[0], location[1] )
                        nodes.append(node)
                        last_node.addArc(ArcType.uninterrupted, node, 0,(node.kilometer - last_node.kilometer))
                        end_of_toll = copy.copy(node)
                        last_node = node
                        node = end_of_toll
                        nodes.append(node)
                    elif unicodedata.normalize('NFC', element.type) == unicodedata.normalize('NFC', u'trafficLight'):
                        #If the node is interrupted we need the start and end of itself
                        location = element.location.split(',')
                        node = TrafficLightNode(element.id, NodeType.traffic_light,element.red_light.duration, element.red_light.frequency ,element.roads[0].id ,element.roads[0].kilometer, location[0], location[1])
                        nodes.append(node)
                        last_node.addArc(ArcType.uninterrupted, node, 0,(node.kilometer - last_node.kilometer))
                        end_of_tl = copy.copy(node)
                        last_node = node
                        node = end_of_tl
                        nodes.append(node)
                    else:
                        node = Node(element.id, NodeType.ordinary,element.roads[0].id ,element.roads[0].kilometer)
                        nodes.append(node)
                else:
                    # element is a Sensor
                    node = Node(element.id, NodeType.sensor, element.road_id ,element.kilometer, 0, 0)
                    nodes.append(node)
                #Add outer arc to last_node, the type of the arc is determined by the two nodes that conform it
                if last_node != None:
                    arc_type = ArcType.uninterrupted
                    if last_node.nodeType == NodeType.traffic_light and node.nodeType == NodeType.traffic_light:
                        arc_type = ArcType.traffic_light
                    elif last_node.nodeType == NodeType.toll and node.nodeType == NodeType.toll:
                        arc_type = ArcType.toll
                    last_node.addArc(arc_type, node, 0,(node.kilometer - last_node.kilometer))
                last_node = node
            # add Finish node to route
            #last_node.addArc(ArcType.uninterrupted, Node('finish '+ key, NodeType.finish, key, 9999), 0,0)
        self.nodes = nodes

    def getFirstNode(self):
        return self.nodes[0]

    def getLastNode(self):
        return self.nodes[len(self.nodes) -1]

    @staticmethod
    def recalculateCost(arc):
        speed = ApiInterface.get_dummy_speed(arc.nodeB.route)
        volume = ApiInterface.get_dummy_volume(arc.nodeB.route)
        arc.cost = CostCalculator.calculeUninterruptedCost(speed, volume)
"""
    def scheduleRecalculations(self):
        while True:
            yield self.env.timeout(self.recalculationStep)
            print "Recalculation of costs, time {0}".format(self.env.now)
            for node in self.nodes:
                for arc in node.outArcs:
                    if(arc.type == ArcType.uninterrupted):
                        self.recalculateCost(arc)
"""