from entities.Arc import ArcType


class Graph(object):
    def __init__(self, nodes, env, recalculationStep):
        self.nodes = nodes
        self.env = env
        self.recalculationStep = recalculationStep
        self.process = env.process(self.scheduleRecalculations())

    def getFirstNode(self):
        return self.nodes[0]

    def recalculateCost(self,arc):
        if arc.type == ArcType.uninterrupted:
            #Recalculate uninterrupted cost based on traffic theory
            if(arc.cost != 1):
                arc.cost += 0.01
        elif arc.type == ArcType.toll:
            #Recalculate interrupted cost based on queue theory
            return
        elif arc.type == ArcType.traffic_light:
            #Recalculate interrupted cost based on queue theory
            return

    def scheduleRecalculations(self):
        while True:
            yield self.env.timeout(self.recalculationStep)
            print "Recalculation of costs, time {0}".format(self.env.now)
            for node in self.nodes:
                for arc in node.outArcs:
                    self.recalculateCost(arc)



		
