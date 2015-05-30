__author__ = 'alfredo'
import simpy

from entities import Car


"""
Simple simpy example

"""
def driver(env, car):
    yield env.timeout(3)
    car.action.interrupt()

env = simpy.Environment()
car = Car(env)
env.process(driver(env, car))
env.run(until=15)