import random
from PyQt4 import QtGui, QtCore
from entities.Node import NodeType

WINDOW_LEFT_PADDING = 80
WINDOW_TOP_PADDING = 380

WIDTH_CONSTANT = 12
HEIGHT_CONSTANT = 12

NODE_RADIUS = 13
LINE_WEIGHT = 8

ICON_DIMENSION = 35

reader= QtGui.QImageReader("semaphore.png")
semImage=reader.read()

reader= QtGui.QImageReader("toll.png")
tollImage=reader.read()

class Drawer(QtGui.QWidget):
    
    def __init__(self, graph):
        super(Drawer, self).__init__()
        self.initUI()
        self.graph = graph

    def initUI(self):      
        self.showFullScreen()
        self.setWindowTitle('Graph')
        self.show()

    def drawImage(self, qp, image,  x, y):
        qp.drawImage(QtCore.QRect((x*WIDTH_CONSTANT) - (ICON_DIMENSION/2) + WINDOW_LEFT_PADDING,(-y*HEIGHT_CONSTANT) - (ICON_DIMENSION/2) + WINDOW_TOP_PADDING, ICON_DIMENSION, ICON_DIMENSION), image)

    def drawNode(self, qp, x, y, color):
        qp.setPen(color)
        qp.setBrush(color)
        qp.drawEllipse((x*WIDTH_CONSTANT) + WINDOW_LEFT_PADDING, (-y*HEIGHT_CONSTANT) + WINDOW_TOP_PADDING, NODE_RADIUS, NODE_RADIUS)
        
    def drawPoint(self, qp, x, y, color):
        qp.setPen(color)
        qp.drawPoint(x, y)    

    def drawLine(self, qp, x, y, x2, y2,  color, color2):
        pen = QtGui.QPen(color, LINE_WEIGHT, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine((x*WIDTH_CONSTANT) + (NODE_RADIUS/2) + WINDOW_LEFT_PADDING, (-y*HEIGHT_CONSTANT) + (NODE_RADIUS/2) + WINDOW_TOP_PADDING, (x2*WIDTH_CONSTANT) + (NODE_RADIUS/2) + WINDOW_LEFT_PADDING, (-y2*HEIGHT_CONSTANT)+ (NODE_RADIUS/2) + WINDOW_TOP_PADDING)

        pen = QtGui.QPen(color2, LINE_WEIGHT-4, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine((x*WIDTH_CONSTANT) + (NODE_RADIUS/2) + WINDOW_LEFT_PADDING, (-y*HEIGHT_CONSTANT) + (NODE_RADIUS/2) + WINDOW_TOP_PADDING, (x2*WIDTH_CONSTANT) + (NODE_RADIUS/2) + WINDOW_LEFT_PADDING, (-y2*HEIGHT_CONSTANT)+ (NODE_RADIUS/2) + WINDOW_TOP_PADDING)


    def paintGrass(self, qp):
        # Paint grass
        size = self.size()
        for i in range(700000):
            color = QtGui.QColor(51, 204, 51)
            x = random.randint(1, size.width()-1)
            y = random.randint(1, size.height()-1)
            self.drawPoint(qp, x, y, color)

        for i in range(550000):
            color = QtGui.QColor(0, 102, 0)
            x = random.randint(1, size.width()-1)
            y = random.randint(1, size.height()-1)
            self.drawPoint(qp, x, y, color)

        for i in range(250000):
            color = QtGui.QColor(102, 255, 51)
            x = random.randint(1, size.width()-1)
            y = random.randint(1, size.height()-1)
            self.drawPoint(qp, x, y, color)

    def paintGraph(self, qp):
        gray = QtGui.QColor(87, 87, 87)
        darkgray = QtGui.QColor(71, 71, 71)
        lightgray = QtGui.QColor(131, 131, 131)

        node = self.graph.getFirstNode()
        arcs = node.outArcs
        visitedNodes = []

        while len(arcs) != 0 :
            arc = arcs.pop()
            self.drawLine(qp, int(arc.nodeA.x), int(arc.nodeA.y), int(arc.nodeB.x), int(arc.nodeB.y), darkgray, lightgray)
            if not arc.nodeB in visitedNodes:
                arcs.extend(arc.nodeB.outArcs)
                visitedNodes.append(arc.nodeB)

        for node in self.graph.nodes:
            if node.nodeType == NodeType.traffic_light:
                self.drawImage(qp, semImage, int(node.x), int(node.y))
            elif node.nodeType == NodeType.toll:
                self.drawImage(qp, tollImage, int(node.x), int(node.y))
            elif node.nodeType == NodeType.fork:
                self.drawNode(qp, int(node.x), int(node.y), gray)


    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        #self.paintGrass(qp)
        self.paintGraph(qp)

        qp.end()

