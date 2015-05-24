import simpy
import random
from Graph import Graph
from Node import Node, NodeType

AVG_SPEED = 100
SPEED_SIGMA = 20

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
                arc = self.position.arcs[0]
                yield self.env.timeout(self.calcNextEventTime(arc))
                self.position = arc.nodeB

            elif self.position.nodeType == NodeType.fork:
                print "Fork of car {0}, node {1}, time {2}".format(self.carId, self.position.nodeId, self.env.now)
                arcs = self.position.arcs
                arc = arcs[random.randint(0,len(arcs)-1)]
                yield self.env.timeout(self.calcNextEventTime(arc))
                self.position = arc.nodeB

            elif self.position.nodeType == NodeType.finish:
                break

    def calcNextEventTime(self, arc):
        """ Calculate the time until next node, recalculating the speed and the distance of the arc. """
        return arc.distance / (1 - arc.cost) * self.speed

        

   