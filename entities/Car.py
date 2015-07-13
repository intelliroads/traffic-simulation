import random
from api_interface.ApiInterface import ApiInterface
from entities.Arc import ArcType
from Node import NodeType
from enum import Enum
import costs.Dijkstra

DETECTOR_DISTANCE = 1.5
ROUTE_MAX_SERVICE = 650
AVG_SPEED = 100
SPEED_SIGMA = 15

class CarType(Enum):
    random = 1
    intelligent = 2

class Car(object):
    def __init__(self, env, carId, position, graph, startTime, type, destination = None):
        self.env = env
        self.startTime = startTime
        self.travelTime = 0
        self.carId = carId
        self.speed = random.gauss(AVG_SPEED, SPEED_SIGMA)
        self.position = position
        self.graph = graph
        self.process = env.process(self.simulate(env))
        self.type = type
        self.destination = destination
        self.readings = 0
        self.driving = False
        self.last_known_position = self.position

    def simulate(self, env):
        yield self.env.timeout(self.startTime)

        self.driving = True
        while True:
            if self.position.nodeType == NodeType.sensor:
                if self.type == CarType.intelligent:
                    print "Post of car {0}, roads {1}, time {2}".format(self.carId, self.position.roads, self.env.now)
                arc = self.position.outArcs[0]
                new_speed = (1-arc.cost) * self.speed
                period = DETECTOR_DISTANCE / self.speed
                delta = int(self.env.now * 3600000)
                time = self.graph.simulation_start_time + delta
                ApiInterface.post_reading(arc.nodeB.nodeId, new_speed, period, time)
                self.readings += 1
            elif self.position.nodeType == NodeType.traffic_light or self.position.nodeType == NodeType.toll:
                #print "Interrupted spot reached by car {0}, roads {1}, time {2}".format(self.carId,self.position.roads, self.env.now)
                arc = self.position.outArcs[0]
            elif self.position.nodeType == NodeType.ordinary:
                #print "Car {0} arrived at location {1}".format(self.carId, arc.nodeB.route)

                arc = arcs[0]
            elif self.position.nodeType == NodeType.fork:
                #print "Fork of car {0}, roads {1}, time {2}".format(self.carId, self.position.roads, self.env.now)
                arcs = self.position.outArcs

                if len(arcs) == 0:
                    #print "Car {0} arrived at destination".format(self.carId)
                    self.travelTime = env.now - self.startTime
                    self.driving = False
                    break

                if self.type == CarType.random:
                    if len(arcs) == 1:
                        arc = arcs[0]
                    else:
                        arc = arcs[random.randint(0,len(arcs)-1)]
                elif self.type == CarType.intelligent:
                    #Calculate shortest path based on graphs costs.
                    path = costs.Dijkstra.dijkstra(self)
                    destinationNode = path[1]
                    for outArc in self.position.outArcs:
                        if outArc.nodeB.nodeId == destinationNode.nodeId:
                            arc = outArc
                            break
            elif self.position == self.destination:
                #print "Car {0} arrived at destination".format(self.carId)
                self.travelTime = env.now - self.startTime
                self.driving = False
                break
            elif self.position.nodeType == NodeType.finish:
                #print "Car {0} out of map".format(self.carId)
                break
            yield self.env.timeout(self.calc_next_event_time(arc))
            self.position = arc.nodeB

            if self.position.nodeType != NodeType.sensor:
                self.last_known_position = self.position


    def calc_next_event_time(self, arc):
        """ Calculate the time until next node, recalculating the speed and the distance of the arc. """
        if arc.type == ArcType.uninterrupted:
            time = self.average_time_uninterrupted(arc.distance, arc.cost, self.speed)
        elif arc.type == ArcType.traffic_light:
            to_time = self.graph.simulation_start_time
            from_time = self.graph.simulation_start_time - 3600000
            road = arc.nodeA.roads.keys()[0]
            flow = ApiInterface.get_volume(road, arc.nodeA.roads[road], from_time, to_time)
            time = self.average_time_in_tls(flow, arc.nodeA.duration,arc.nodeA.frequency)
        else:
            delta = int(self.env.now * 3600000)
            to_time = self.graph.simulation_start_time + delta
            from_time = self.graph.simulation_start_time + delta - 3600000
            road = arc.nodeA.roads.keys()[0]
            flow = ApiInterface.get_volume(road, arc.nodeA.roads[road], from_time, to_time)
            time = self.average_time_in_toll(flow, arc.nodeB.service_rate, arc.nodeB.servers)

        return time


    def average_time_uninterrupted(self,arc_distance, arc_cost, car_speed):
        return arc_distance / ((1-arc_cost) * float(car_speed))


    def average_time_in_toll(self, arrival_rate, service_rate, servers):
        """
         Calculates the average time in a toll

         Args:
           arrival_rate (float): total arrival rate of de route, combining the flow of each lane. Expressed as vehicles/hour.
           service_rate(float): service rate of normal windows, expressed as vehicles/hours.
           windows(int): number of windows at the toll.
        """
        # Split normal arrival rate for each window to model each individual M/M/1 queue
        arrival_rate_foreach_server = float(arrival_rate) / servers

        if arrival_rate_foreach_server == 0:
            return 1. / service_rate

        traffic_intensity = float(arrival_rate_foreach_server) / service_rate
        vehicles_in_system_per_window = float(traffic_intensity) / (1.0 - traffic_intensity)
        time_in_system = float(vehicles_in_system_per_window) / arrival_rate_foreach_server
        return float(time_in_system) / 3600


    def average_time_in_tls(self, total_arrival_rate, red_light_duration, red_light_frequency):
        """
         Calculates the average time in a traffic light signal using queue theory
        """
        service_rate = ROUTE_MAX_SERVICE * (red_light_frequency / float(red_light_duration + red_light_frequency))
        traffic_intensity = float(total_arrival_rate) / service_rate
        time_in_queue = traffic_intensity / float(service_rate * (1 - traffic_intensity))
        service_time = red_light_duration * (red_light_duration / float(red_light_duration + red_light_frequency))
        return float(time_in_queue + service_time) / 3600
