import random
import sys
import simpy
import thread
import time
from datetime import  datetime
from entities.Graph import Graph
from entities.Car import Car, CarType
from utils import ColorInterpolator
from PyQt4 import QtGui
from GUI import Drawer

NUM_CARS = 1

def createGraph(env, simulation_start_time):
    return Graph(env, simulation_start_time)


def simulate():
    env.run(until=1000)

def repaint_graph(drawer):
    while True:
        time.sleep(1)
        drawer.readings = sum([car.readings for car in cars])
        drawer.driving = sum([car.driving for car in cars])
        drawer.time = "%.2f" % env.now
        drawer.update()


env = simpy.Environment()

# Save simulation starttime
simulation_start_time = int((datetime.now() - datetime(1970,1,1)).total_seconds() * 1000)

graph = createGraph(env, simulation_start_time)
color_interpolator = ColorInterpolator.ColorInterpolator()
app = QtGui.QApplication(sys.argv)
cars = [Car(env, i, graph.getFirstNode(), graph, random.expovariate(0.05), CarType.random) for i in range(NUM_CARS)]

# Start simulation in other thread
thread.start_new_thread(simulate, ())

drawer = Drawer(graph, color_interpolator)

# Daemon that repaints graph
thread.start_new_thread(repaint_graph, (drawer,))

sys.exit(app.exec_())




