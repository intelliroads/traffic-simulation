import os

import fuzzy.storage.fcl.Reader


class CostCalculator(object):
    """
    This class is used to calculate uninterrupted arcs costs using fuzzy logic
    """
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
