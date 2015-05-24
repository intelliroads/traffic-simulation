from Node import Node


class Graph(object):
    def __init__(self, nodes, env, recalculationStep):
        self.nodes = nodes
        self.env = env
        self.recalculationStep = recalculationStep
        self.process = env.process(self.scheduleRecalculations())

    def getFirstNode(self):
        return self.nodes[0]

    def recalculateCost(self,arc):
        if(arc.cost != 1):
            arc.cost += 0.01

    def scheduleRecalculations(self):
        while True:
            yield self.env.timeout(self.recalculationStep)
            print "Recalculation of costs, time {0}".format(self.env.now)
            for node in self.nodes:
                for arc in node.arcs:
                    self.recalculateCost(arc)



		
