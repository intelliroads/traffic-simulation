from Graph import Graph
from Node import Node, NodeType
from Car import Car
import random
import simpy

NUM_CARS = 100


def createGraph(env):
	nodes = []

	n1 = Node(1,NodeType.sensor)
	n2 = Node(2,NodeType.sensor)
	n3 = Node(3,NodeType.sensor)
	n4 = Node(4,NodeType.fork)
	n5 = Node(5,NodeType.sensor)
	n6 = Node(6,NodeType.sensor)
	n7 = Node(7,NodeType.sensor)
	n8 = Node(8,NodeType.sensor)
	n9 = Node(9,NodeType.fork)
	n10 = Node(10,NodeType.sensor)
	n11 = Node(11,NodeType.sensor)
	n12 = Node(12,NodeType.finish)

	nodes.append(n1)
	nodes.append(n2)
	nodes.append(n3)
	nodes.append(n4)
	nodes.append(n5)
	nodes.append(n6)
	nodes.append(n7)
	nodes.append(n8)
	nodes.append(n9)
	nodes.append(n10)
	nodes.append(n11)
	nodes.append(n12)

	n1.addArc(n2,0,0.5)
	n2.addArc(n3,0,0.5)
	n3.addArc(n4,0,0.5)
	n4.addArc(n5,0,0.5)
	n4.addArc(n7,0,0.5)
	n4.addArc(n5,0,0.5)
	n5.addArc(n6,0,0.5)
	n6.addArc(n9,0,0.5)
	n7.addArc(n8,0,0.5)
	n8.addArc(n9,0,0.5)
	n9.addArc(n10,0,0.5)
	n10.addArc(n11,0,0.5)
	n11.addArc(n12,0,0.5)

	return Graph(nodes,env,100)

env = simpy.Environment()
graph = createGraph(env)
cars = [Car(env, i, graph.getFirstNode(), graph, random.expovariate(0.001)) for i in range(NUM_CARS)]
env.run(until = 10000)
