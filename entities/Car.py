import random

from entities.Arc import ArcType
from Node import NodeType


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
                print "Post of car {0}, node {1}, time {2}".format(self.carId, self.position.nodeId, self.env.now)
                arc = self.position.outArcs[0]
                yield self.env.timeout(self.calcNextEventTime(arc))
                self.position = arc.nodeB

            elif self.position.nodeType == NodeType.fork:
                print "Fork of car {0}, node {1}, time {2}".format(self.carId, self.position.nodeId, self.env.now)
                arcs = self.position.outArcs
                arc = arcs[random.randint(0,len(arcs)-1)]
                yield self.env.timeout(self.calcNextEventTime(arc))
                self.position = arc.nodeB

            elif self.position.nodeType == NodeType.finish:
                print "Car {0} arrived at destination".format(self.carId)
                break

    def calcNextEventTime(self, arc):
        """ Calculate the time until next node, recalculating the speed and the distance of the arc. """
        if(arc.type == ArcType.uninterrupted):
            time = self.average_time_uninterrupted(arc.distance, arc.cost, self.speed)
        elif(arc.type == ArcType.traffic_light):
            flow = 0 #GET FLOW FROM API
            time = self.average_time_in_tls(flow,arc.nodeA.saturation_rate,arc.nodeA.effective_red_time)
        else:
            flow = 0 #GET FLOW FROM API
            time = self.average_time_in_toll(flow, arc.nodeA.windows, arc.nodeA.service_rate)
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


    def average_time_in_tls(self, total_arrival_rate, saturation_rate, effective_red_time):
        """
         Calculates the average time in a traffic light signal using vehicular flow theory.

         Args:
           total_arrival_rate (float): total arrival rate of de route, combining the flow of each lane. Expressed as vehicles/hour.
           saturation_rate(float): max service rate of the lane, it is reached when the traffic light goes green.
           effective_red_time (float): effective red time in seconds within a traffic light cycle.
        """
        return saturation_rate * effective_red_time / (saturation_rate - total_arrival_rate)

