import random
from api_interface.ApiInterface import ApiInterface
from entities.Arc import ArcType
from Node import NodeType
from Graph import Graph
from datetime import datetime,timedelta

DETECTOR_DISTANCE = 1.5
ROUTE_MAX_SERVICE = 650
AVG_SPEED = 50
SPEED_SIGMA = 5

class Car(object):
    def __init__(self, env, carId, position, graph, startTime):
        self.env = env
        self.startTime = startTime
        self.carId = carId
        self.speed = random.gauss(AVG_SPEED, SPEED_SIGMA)
        self.position = position
        self.graph = graph
        self.process = env.process(self.simulate(env))

    def simulate(self, env):
        yield self.env.timeout(self.startTime)

        while True:
            if self.position.nodeType == NodeType.sensor:
                print "Post of car {0}, route {1}, kilometer {2}, time {3}".format(self.carId, self.position.route,self.position.kilometer, self.env.now)
                arc = self.position.outArcs[0]
                new_speed = (1-arc.cost) * self.speed
                period = DETECTOR_DISTANCE / self.speed
                ApiInterface.post_reading(arc.nodeB.nodeId, new_speed, period)
            elif self.position.nodeType == NodeType.traffic_light or self.position.nodeType == NodeType.toll:
                print "Interrupted spot reached by car {0}, time {1}".format(self.carId, self.env.now)
                arc = self.position.outArcs[0]
            elif self.position.nodeType == NodeType.ordinary:
                print "Car {0} arrived at location {1}".format(self.carId, arc.nodeB.route)
                arc = arcs[0]
            elif self.position.nodeType == NodeType.fork:
                print "Fork of car {0}, node {1}, time {2}".format(self.carId, self.position.nodeId, self.env.now)
                arcs = self.position.outArcs
                arc = arcs[random.randint(0,len(arcs)-1)]
            elif self.position.nodeType == NodeType.finish:
                print "Car {0} arrived at destination".format(self.carId)
                break
            yield self.env.timeout(self.calcNextEventTime(arc))
            if(arc.type == ArcType.uninterrupted):
                Graph.recalculateCost(arc)
            self.position = arc.nodeB


    def calcNextEventTime(self, arc):
        """ Calculate the time until next node, recalculating the speed and the distance of the arc. """
        if arc.type == ArcType.uninterrupted:
            time = self.average_time_uninterrupted(arc.distance, arc.cost, self.speed)
        elif arc.type == ArcType.traffic_light:
            flow = ApiInterface.get_dummy_volume(arc.nodeB.route)
            time = self.average_time_in_tls(flow,arc.nodeA.duration,arc.nodeA.frequency)
        else:
            flow = ApiInterface.get_dummy_volume(arc.nodeB.route)
            time = self.average_time_in_toll(flow, arc.nodeA.servers, arc.nodeA.service_rate)
        return time;


    def average_time_uninterrupted(self,arc_distance, arc_cost, car_speed):
        return arc_distance / ((1-arc_cost) * car_speed)


    def average_time_in_toll(self, arrival_rate, service_rate, servers):
        """
         Calculates the average time in a toll

         Args:
           arrival_rate (float): total arrival rate of de route, combining the flow of each lane. Expressed as vehicles/hour.
           service_rate(float): service rate of normal windows, expressed as vehicles/hours.
           windows(int): number of windows at the toll.
        """
        # Split normal arrival rate for each window to model each individual M/M/1 queue
        arrival_rate_foreach_server = arrival_rate / servers
        traffic_intensity = arrival_rate_foreach_server / service_rate
        vehicles_in_system_per_window = traffic_intensity / (1.0 - traffic_intensity)
        time_in_system = vehicles_in_system_per_window / arrival_rate_foreach_server
        return time_in_system


    def average_time_in_tls(self, total_arrival_rate,red_light_duration, red_light_frequency):
        """
         Calculates the average time in a traffic light signal using vehicular flow theory.
        """
        effective_red_light = red_light_duration / (red_light_duration + red_light_frequency)
        return ROUTE_MAX_SERVICE * effective_red_light / (ROUTE_MAX_SERVICE - total_arrival_rate)
