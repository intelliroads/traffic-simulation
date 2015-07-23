import random
import math
from enum import Enum

from api_interface.ApiInterface import ApiInterface
from entities.Arc import ArcType
from Node import NodeType
import costs.Dijkstra

# Distance in kilometers between two sensors within a speed trap
DETECTOR_DISTANCE = 0.0015
# Saturation flow of the road
ROUTE_MAX_SERVICE = 650
# Average car's desired speed
AVG_SPEED = 110
# Sigma of car's desired speed
SPEED_SIGMA = 10


class CarType(Enum):
    """Possible types of cars:
    - random: When faced with a decision, the car will take a random road.
    - intelligent: When faced with a decision, the car will take the optimal road based on Dijkstra's
    algorithms result.
    - forced: The car will always take the path defined in his forcedPath attribute"""
    random = 1
    intelligent = 2
    forced = 3


class Car(object):
    """Representation of a car driving within the route."""
    def __init__(self, env, carId, position, graph, startTime, type, destination=None, forced_path = None):
        self.env = env
        self.startTime = startTime
        self.travelTime = 0
        self.carId = carId
        self.preferred_speed = random.gauss(AVG_SPEED, SPEED_SIGMA)
        self.speed = self.preferred_speed
        self.position = position
        self.graph = graph
        self.process = env.process(self.simulate(env))
        self.type = type
        self.destination = destination
        self.readings = 0
        self.driving = False
        self.last_known_position = self.position
        self.forced_path = forced_path
        self.forks_passed = 0

    def simulate(self, env):
        """Simulation of the trip of a car.

        Keyword arguments:
        env -- Simpy environment to simulate events."""
        yield self.env.timeout(self.startTime)

        self.driving = True
        while True:

            if self.position.nodeType == NodeType.sensor:
                arc = self.position.outArcs[0]
                coef = (math.sqrt(1 - arc.cost ** 2) + 0.1)
                self.speed = coef * self.preferred_speed
                period = DETECTOR_DISTANCE / self.speed
                delta = int(self.env.now * 3600000)
                time = self.graph.simulation_start_time + delta
                ApiInterface.post_reading(self.position, self.speed, period, time)
                self.readings += 1
            elif self.position.nodeType == NodeType.traffic_light or self.position.nodeType == NodeType.toll:
                arc = self.position.outArcs[0]
            elif self.position.nodeType == NodeType.ordinary:
                arc = arcs[0]
            elif self.position.nodeType == NodeType.fork:
                arcs = self.position.outArcs
                if len(arcs) == 0:
                    self.travelTime = env.now - self.startTime
                    self.driving = False
                    break
                if self.type == CarType.random:
                    if len(arcs) == 1:
                        arc = arcs[0]
                    else:
                        arc = arcs[random.randint(0, len(arcs) - 1)]
                elif self.type == CarType.intelligent:
                    #Calculate shortest path based on graphs costs.
                    path = costs.Dijkstra.dijkstra(self)
                    destinationNode = path[1]
                    for outArc in self.position.outArcs:
                        if outArc.nodeB.nodeId == destinationNode.nodeId:
                            arc = outArc
                            break
                elif self.type == CarType.forced:
                    index = 0
                    #Safety checks
                    if len(self.forced_path) > self.forks_passed and len(arcs) > self.forced_path[self.forks_passed]:
                        index = self.forced_path[self.forks_passed]
                    arc = arcs[index]
                    self.forks_passed += 1
            elif self.position == self.destination:
                self.travelTime = env.now - self.startTime
                self.driving = False
                break
            elif self.position.nodeType == NodeType.finish:
                break
            delay = self.calc_next_event_time(arc)
            yield self.env.timeout(delay if delay > 0 else 0)
            self.position = arc.nodeB
            if self.position.nodeType != NodeType.sensor:
                self.last_known_position = self.position


    def calc_next_event_time(self, arc):
        """ Calculate the time until next node, recalculating the speed and the distance of the arc.

        Keyword arguments:
        arc -- Arc traversed by the car."""
        if arc.type == ArcType.uninterrupted:
            time = self.average_time_uninterrupted(arc.distance, self.speed)
        elif arc.type == ArcType.traffic_light:
            to_time = self.graph.simulation_start_time
            from_time = self.graph.simulation_start_time - 3600000
            road = arc.nodeA.roads.keys()[0]
            flow = ApiInterface.get_volume(road, arc.nodeA.roads[road], from_time, to_time)
            time = self.average_time_in_tls(flow, arc.nodeA.duration, arc.nodeA.frequency)
        else:
            delta = int(self.env.now * 3600000)
            to_time = self.graph.simulation_start_time + delta
            from_time = self.graph.simulation_start_time + delta - 3600000
            road = arc.nodeA.roads.keys()[0]
            flow = ApiInterface.get_volume(road, arc.nodeA.roads[road], from_time, to_time)
            time = self.average_time_in_toll(flow, arc.nodeB.service_rate, arc.nodeB.servers)

        return time


    def average_time_uninterrupted(self, arc_distance, car_speed):
        """Calculates average time for uninterrupted sections.

        Keyword arguments:
        arc_distance -- Distance of the arc traversed by the car.
        car_speed -- Current speed of the car."""
        return float(arc_distance) / car_speed


    def average_time_in_toll(self, arrival_rate, service_rate, servers):
        """Calculates the average time in a toll.

        Keyword arguments:
        arrival_rate: total arrival rate of de route, combining the flow of each lane. Expressed as vehicles/hour.
        service_rate: service rate of normal windows, expressed as vehicles/hours.
        windows: number of windows at the toll."""

        # Split normal arrival rate for each window to model each individual M/M/1 queue
        arrival_rate_foreach_server = float(arrival_rate) / servers

        # If the arrival rate is zero, the time in the toll is equal to the service time
        if arrival_rate_foreach_server == 0:
            return 1. / service_rate

        traffic_intensity = float(arrival_rate_foreach_server) / service_rate
        vehicles_in_system_per_window = float(traffic_intensity) / (1.0 - traffic_intensity)
        time_in_system = float(vehicles_in_system_per_window) / arrival_rate_foreach_server
        return float(time_in_system) / 3600


    def average_time_in_tls(self, total_arrival_rate, red_light_duration, red_light_frequency):
        """Calculates the average time in a traffic light signal using queue theory.

        Keyword arguments:
        total_arrival_rate: Arrival rate of the traffic light.
        red_light_duration: Duration of the red light of the traffic light.
        red_light_frequency: Frequency of the red light of the traffic light.
        """
        service_rate = ROUTE_MAX_SERVICE * (red_light_frequency / float(red_light_duration + red_light_frequency))
        traffic_intensity = float(total_arrival_rate) / service_rate
        time_in_queue = traffic_intensity / float(service_rate * (1 - traffic_intensity))
        service_time = red_light_duration * (red_light_duration / float(red_light_duration + red_light_frequency))
        return float(time_in_queue + service_time) / 3600
