import random
import sys
import time
from datetime import datetime

import simpy

import thread
from entities.Graph import Graph
from entities.Car import Car, CarType
from utils import ColorInterpolator
from PyQt4 import QtGui
from GUI import Drawer


NUM_CARS = 2300
SIMULATION_TIME = 25


def createGraph(env, simulation_start_time):
    return Graph(env, simulation_start_time)


def simulate(cars):
    env.run(until=SIMULATION_TIME)

    print
    "Simulation finished"
    random_cars = [car.travelTime for car in cars if
                   (car.type == CarType.random and car.startTime <= 8 and car.travelTime > 0)]
    avg_random_cars = float(sum(random_cars)) / len(random_cars)

    intelligent_cars = [car.travelTime for car in cars if car.type == CarType.intelligent and car.travelTime > 0]
    avg_intelligent_cars = float(sum(intelligent_cars)) / len(intelligent_cars)

    print
    avg_random_cars
    print
    avg_intelligent_cars


def repaint_graph(drawer, graph, ):
    while True:
        if not graph.repaining:
            time.sleep(1)
            drawer.readings = sum([car.readings for car in cars])
            drawer.driving = sum([car.driving for car in cars])
            drawer.time = "%.2f" % env.now
            drawer.update()


env = simpy.Environment()

# Save simulation starttime
simulation_start_time = int((datetime.now() - datetime(1970, 1, 1)).total_seconds() * 1000)
print
simulation_start_time
graph = createGraph(env, simulation_start_time)
color_interpolator = ColorInterpolator.ColorInterpolator()
app = QtGui.QApplication(sys.argv)

car_nro = 0
cars = [Car(env, i + car_nro, graph.getFirstNode(), graph, 0, CarType.random) for i in range(1000)]
car_nro += 1000
cars.extend([Car(env, i + car_nro, graph.getFirstNode(), graph, 2.5, CarType.random) for i in range(800)])
car_nro += 800
cars.extend([Car(env, i + car_nro, graph.getFirstNode(), graph, 5.0, CarType.random) for i in range(800)])
car_nro += 800
cars.extend([Car(env, i + car_nro, graph.getFirstNode(), graph, 8.5, CarType.random) for i in range(750)])
car_nro += 750
cars.extend([Car(env, i + car_nro, graph.getFirstNode(), graph, 11.0, CarType.random) for i in range(750)])
car_nro += 750
cars.extend([Car(env, i + car_nro, graph.getFirstNode(), graph, 13.0, CarType.random) for i in range(400)])
car_nro += 400

cars.extend(
    [Car(env, i + car_nro, graph.getFirstNode(), graph, random.uniform(0, SIMULATION_TIME - 3), CarType.random) for i in
     range(NUM_CARS)])
car_nro += NUM_CARS

cars.extend(
    [Car(env, i + car_nro, graph.getFirstNode(), graph, random.uniform(8, 13), CarType.intelligent, graph.getLastNode())
     for i in range(300)])
car_nro += 200

# Start simulation in other thread
thread.start_new_thread(simulate, (cars,))

drawer = Drawer(graph, color_interpolator, cars)

# Daemon that repaints graph
thread.start_new_thread(repaint_graph, (drawer, graph,))

sys.exit(app.exec_())




