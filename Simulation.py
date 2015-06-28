import random
import sys
import simpy

from entities.Graph import Graph
from entities.Car import Car
from PyQt4 import QtGui, QtCore
from GUI import Drawer


NUM_CARS = 1009


def createGraph(env):
    return Graph(env,100)

env = simpy.Environment()
graph = createGraph(env)

app = QtGui.QApplication(sys.argv)
drawer = Drawer(graph)


sys.exit(app.exec_())

#cars = [Car(env, i, graph.getFirstNode(), graph, random.expovariate(0.001)) for i in range(NUM_CARS)]
#env.run(until = 10000)
