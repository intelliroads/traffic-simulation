import fuzzy.storage.fcl.Reader
import os


class CostCalculator(object):
    global system

    dir = os.path.dirname(__file__)
    system = fuzzy.storage.fcl.Reader.Reader().load_from_file(dir + "/fuzzydefinitions.fcl")

    @staticmethod
    def calculeUninterruptedCost(speed, volume):
        my_input = {
            "Speed": speed,
            "DeltaVolume": volume,
        }

        my_output = {
            "Cost": 0.0
        }

        # calculate
        system.calculate(my_input, my_output)
        cost = my_output["Cost"]
        return cost
