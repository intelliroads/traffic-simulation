import unicodedata

from entities.Arc import ArcType
from api_interface.ApiInterface import ApiInterface
from api_interface.Spot import Spot
from entities.Node import Node, TollNode, TrafficLightNode, NodeType
from costs.CostCalculator import CostCalculator


class Graph(object):
    """Representation of the road as a directed graph."""

    def __init__(self, env, simulation_start_time):
        self.env = env
        self.simulation_start_time = simulation_start_time
        self.process = env.process(self.simulate(env))
        self.repainting = False
        spots = ApiInterface.get_all_spots()
        sensors = ApiInterface.get_all_sensors()
        self.nodes = []
        self.initNodes(spots, sensors)

    """

    """

    def simulate(self, env):
        """Schedule of recalculation events to recalculate arcs costs.

        Keyword arguments:
        env -- Simpy env for the simulation of events.
        """
        while True:
            yield env.timeout(0.10)
            self.recalculate_graph()

    def initNodes(self, spots, sensors):
        """Initialize the graph's nodes using the information fetched from the api.

        Keyword arguments:
        spots -- Spots of interest fetched from the api.
        sensors -- Sensors located in the roads, fetched from the api.
        """
        dict = {}
        # Creation of dictionary to store spots_list of sensors and spots by roadId
        for spot in spots:
            for road in spot.roads:
                if not dict.has_key(road.id):
                    dict[road.id] = []
                dict[road.id].append(spot)
        for sensor in sensors:
            if not dict.has_key(sensor.road_id):
                dict[sensor.road_id] = []
            dict[sensor.road_id].append(sensor)
        # Order sub lists by kilometer
        for key in dict.keys():
            dict[key].sort(key=lambda x: x.get_kilometer_of_route(key) if isinstance(x, Spot) else x.kilometer,
                           reverse=False)

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
                        node = next((x for x in forkNodes if x.nodeId == element.id), None)
                        if node == None:
                            location = element.location.split(',')
                            roads = {road.id: road.kilometer for road in element.roads}
                            node = Node(element.id, NodeType.fork, roads, location[0], location[1])
                            nodes.append(node)
                            forkNodes.append(node)
                    elif unicodedata.normalize('NFC', element.type) == unicodedata.normalize('NFC', u'toll'):
                        # If the node is interrupted we need the start and end of itself
                        location = element.location.split(',')
                        roads = {road.id: road.kilometer for road in element.roads}
                        node = TollNode(element.id, NodeType.toll, element.toll.number_of_servers,
                                        element.toll.service_rate, roads, location[0], location[1])
                        nodes.append(node)

                        road = None
                        for key in node.roads.keys():
                            if last_node.roads.has_key(key):
                                road = key
                                break
                        last_node.addArc(ArcType.uninterrupted, node, 0, (node.roads[road] - last_node.roads[road]))
                        end_of_toll = TollNode(element.id + "x", NodeType.toll, element.toll.number_of_servers,
                                               element.toll.service_rate, roads, location[0], location[1])
                        last_node = node
                        node = end_of_toll
                        nodes.append(node)
                    elif unicodedata.normalize('NFC', element.type) == unicodedata.normalize('NFC', u'trafficLight'):
                        # If the node is interrupted we need the start and end of itself
                        location = element.location.split(',')
                        roads = {road.id: road.kilometer for road in element.roads}
                        node = TrafficLightNode(element.id, NodeType.traffic_light, element.red_light.duration,
                                                element.red_light.frequency, roads, location[0], location[1])
                        nodes.append(node)

                        road = None
                        for key in node.roads.keys():
                            if last_node.roads.has_key(key):
                                road = key
                                break
                        last_node.addArc(ArcType.uninterrupted, node, 0, (node.roads[road] - last_node.roads[road]))
                        end_of_tl = TrafficLightNode(element.id + "x", NodeType.traffic_light,
                                                     element.red_light.duration, element.red_light.frequency, roads,
                                                     location[0], location[1])

                        last_node = node
                        node = end_of_tl
                        nodes.append(node)
                    else:
                        roads = {road.id: road.kilometer for road in element.roads}
                        node = Node(element.id, NodeType.ordinary, roads, 0, 0)
                        nodes.append(node)
                else:
                    # element is a Sensor
                    node = Node(element.id, NodeType.sensor, {element.road_id: element.kilometer}, 0, 0)
                    nodes.append(node)
                # Add outer arc to last_node, the type of the arc is determined by the two nodes that conform it
                if last_node != None:
                    arc_type = ArcType.uninterrupted
                    if last_node.nodeType == NodeType.traffic_light and node.nodeType == NodeType.traffic_light:
                        arc_type = ArcType.traffic_light
                    elif last_node.nodeType == NodeType.toll and node.nodeType == NodeType.toll:
                        arc_type = ArcType.toll

                    road = None
                    for key in node.roads.keys():
                        if last_node.roads.has_key(key):
                            road = key
                            break
                    if last_node.roads[road] <= node.roads[road]:
                        last_node.addArc(arc_type, node, 0, (node.roads[road] - last_node.roads[road]))
                last_node = node
        self.nodes = nodes

    def getFirstNode(self):
        """Get initial note of the graph"""
        return self.nodes[0]

    def getLastNode(self):
        """Get last node of the graph"""
        for node in self.nodes:
            if len(node.outArcs) == 0:
                return node


    def recalculate_graph(self):
        """Recalculate graph's arc's costs"""
        self.repainting = True
        node = self.getFirstNode()
        arcs = []
        arcs.extend(node.outArcs)
        visited_nodes = []
        current_node = None
        temp_arcs = []

        while len(arcs) != 0:
            arc = arcs.pop()
            temp_arcs.append(arc)
            if arc.nodeA.nodeType != NodeType.sensor:
                current_node = arc.nodeA
            if arc.nodeB.nodeType != NodeType.sensor:

                delta = int(self.env.now * 3600000)
                to_time = self.simulation_start_time + delta
                from_time = to_time - 3600000

                road = None
                for key in arc.nodeB.roads.keys():
                    if current_node.roads.has_key(key):
                        road = key
                        break

                if (current_node.nodeType == NodeType.traffic_light and arc.nodeB.nodeType == NodeType.traffic_light) \
                        or (current_node.nodeType == NodeType.toll and arc.nodeB.nodeType == NodeType.toll):
                    volume = ApiInterface.get_volume(road, arc.nodeB.roads[road], from_time, to_time)
                    arc.cost = volume
                else:
                    delta_volume = ApiInterface.get_delta_volume(road, current_node.roads[road], arc.nodeB.roads[road],
                                                                 from_time, to_time)
                    speed = ApiInterface.get_speed(road, current_node.roads[road], arc.nodeB.roads[road], from_time,
                                                   to_time)

                    if speed == 0:
                        cost = 0
                    else:
                        cost = CostCalculator.calculeUninterruptedCost(speed, delta_volume)

                    for temp_arc in temp_arcs:
                        temp_arc.cost = cost

                    temp_arcs = []

                current_node = arc.nodeB
            if arc.nodeB not in visited_nodes:
                arcs.extend(arc.nodeB.outArcs)
                visited_nodes.append(arc.nodeB)
        self.repainting = False

