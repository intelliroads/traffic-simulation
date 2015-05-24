from enum import Enum
from Arc import Arc

class NodeType(Enum):
	sensor = 1
	fork = 2
	finish = 3

class Node(object):

	def __init__(self, nodeId, nodeType):
		self.nodeType = nodeType
		self.nodeId = nodeId
		self.arcs = []

	def addArc(self, nodeB, cost, distance):
		self.arcs.append(Arc(self,nodeB, cost, distance))

