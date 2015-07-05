import random
import sys
import simpy
from entities.Graph import Graph
from entities.Car import Car, CarType
from PyQt4 import QtGui
from GUI import Drawer


NUM_CARS = 10


def createGraph(env):
    return Graph(env,100)

env = simpy.Environment()
graph = createGraph(env)

#app = QtGui.QApplication(sys.argv)
#drawer = Drawer(graph)
#sys.exit(app.exec_())

cars = [Car(env, i, graph.getFirstNode(), graph, random.expovariate(0.01), CarType.random) for i in range(NUM_CARS)]
env.run(until=1000)


