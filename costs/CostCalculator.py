import fuzzy.storage.fcl.Reader
import os

class CostCalculator(object):
	global system

	dir = os.path.dirname(__file__)
	system =  fuzzy.storage.fcl.Reader.Reader().load_from_file(dir + "/fuzzydefinitions.fcl")
 

	@staticmethod
	def calculeUninterruptedCost(speed, volume):	

		my_input = {
	        "Velocidad" : speed,
	        "Volumen" : volume,
        }

		my_output = {
		        "Costo" : 0.0
		        }

		# calculate
		system.calculate(my_input, my_output)
		cost = my_output["Costo"]
		return cost

		