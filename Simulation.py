import random

import simpy
from entities.Graph import Graph
from entities.Car import Car, CarType

NUM_CARS = 10


def createGraph(env):
	return Graph(env,100)

env = simpy.Environment()
graph = createGraph(env)
cars = [Car(env, i, graph.getFirstNode(), graph, random.expovariate(0.001),CarType.random) for i in range(NUM_CARS)]
Car(env, i+1, graph.getFirstNode(),graph, 5, CarType.intelligent, graph.getLastNode())
env.run(until = 10000)


