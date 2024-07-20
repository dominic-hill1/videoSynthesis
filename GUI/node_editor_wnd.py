from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from node_scene import Scene
from node_node import SinOscNode, SquareOscNode, ColorMixerNode, ColorAddNode, ColorMultNode, SliderNode, OutputNode, FeedbackZoomNode, LumaKeyNode
from node_edge import Edge, EDGE_TYPE_BEZIER
from node_graphics_view import QDMGraphicsView


class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stylesheet_filename = 'qss/nodestyle.qss'
        self.loadStylesheet(self.stylesheet_filename)

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Create graphics scene
        self.scene = Scene()
        # self.grScene = self.scene.grScene


        self.addNodes()

        # Create graphics view
        self.view = QDMGraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Video synthesiser")
        self.show()

    def addNodes(self):
        node1 = SinOscNode(self.scene)
        node2 = ColorMultNode(self.scene)
        node3 = SquareOscNode(self.scene)
        node4 = ColorMixerNode(self.scene)
        node5 = SliderNode(self.scene)
        node6 = OutputNode(self.scene)
        node7 = FeedbackZoomNode(self.scene)
        node8 = LumaKeyNode(self.scene)

        node1.setPos(-350, -250)
        node2.setPos(-75, 0)
        node3.setPos(200, -150)
        node4.setPos(300, 300)
        node5.setPos(100, 300)
        node6.setPos(300, 200)
        node7.setPos(100, 100)
        node8.setPos(200, 150)

        edge1 = Edge(self.scene, node1.outputs[0], node2.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        edge2 = Edge(self.scene, node2.outputs[0], node3.inputs[2], edge_type=EDGE_TYPE_BEZIER)
        
    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)
        rect = self.grScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)
    
        text = self.grScene.addText("This is some text", QFont("Ubuntu"))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        widget1 = QPushButton("Hello world")
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = self.grScene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(0, 60)

        line = self.grScene.addLine(-200, -100, 400, 200, outlinePen)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)

    def loadStylesheet(self, filename):
        print("Style loading:", filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))
