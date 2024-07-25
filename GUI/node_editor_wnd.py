from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import subprocess

from node_scene import Scene
from node_node import *
from node_edge import Edge, EDGE_TYPE_BEZIER
from node_graphics_view import QDMGraphicsView
from node_sidebar import Sidebar


class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stylesheet_filename = 'qss/nodestyle.qss'
        self.loadStylesheet(self.stylesheet_filename)
    
        self.nodes = []
        self.edges = []

        self.initUI()

    
 

    def initUI(self):
        # self.setGeometry(200, 200, 800, 600)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # Create graphics scene
        self.scene = Scene()
        self.sidebar = Sidebar(self)
        # self.grScene = self.scene.grScene


        self.addNodes()

        # Create graphics view
        self.view = QDMGraphicsView(self.scene.grScene, parent=self)
        # self.view.setGeometry(0, 0, 1920, 1080)
        # self.sidebar.setGeometry(1700, 0, 1920, 1080)
        self.layout.addWidget(self.view)
        self.layout.addWidget(self.sidebar)

        self.setWindowTitle("Video synthesiser")
        self.show()

    def addNodes(self):
        # self.nodes.append(SinOscNode(self.scene))
        # self.nodes.append(ColorMixerNode(self.scene))
        # self.nodes.append(SquareOscNode(self.scene))
        self.nodes.append(OutputNode(self.scene))
        self.nodes.append(LargeSliderNode(self.scene))
        self.nodes.append(LargeSliderNode(self.scene))
        self.nodes.append(LargeSliderNode(self.scene))
        self.nodes.append(SmallSliderNode(self.scene))
        self.nodes.append(SmallSliderNode(self.scene))
        self.nodes.append(SmallSliderNode(self.scene))
        # self.nodes.append(ColorXNode(self.scene))
        # self.nodes.append(AddNode(self.scene))
        # self.nodes.append(MultiplyNode(self.scene))
        # node4 = ColorMixerNode(self.scene)
        # node5 = SliderNode(self.scene)
        # node6 = OutputNode(self.scene)
        # node7 = FeedbackZoomNode(self.scene)
        # node8 = LumaKeyNode(self.scene)
        # node9 = ColorDisplaceNode(self.scene)
        # node10 = SliderNode(self.scene)
        # node11 = SliderNode(self.scene)
        # node12 = ColorMixerNode(self.scene)

        self.nodes[0].setPos(350, 250)
        self.nodes[1].setPos(-350, -250)
        self.nodes[2].setPos(-350, -250)
        self.nodes[3].setPos(-350, -250)
        self.nodes[4].setPos(-350, -250)
        self.nodes[5].setPos(-350, -250)
        self.nodes[6].setPos(-350, -250)
        # self.nodes[1].setPos(-75, 0)
        # self.nodes[2].setPos(200, -150)
        # self.nodes[3].setPos(250, 200)
        # node4.setPos(300, 300)
        # node5.setPos(100, 300)
        # node6.setPos(300, 200)
        # node7.setPos(100, 100)
        # node8.setPos(200, 150)
        # node9.setPos(200, 150)
        # node10.setPos(200, 150)
        # node11.setPos(200, 150)
        # node12.setPos(200, 150)

        # self.edges.append(Edge(self.scene, self.nodes[0].outputs[0], self.nodes[1].inputs[0], edge_type=EDGE_TYPE_BEZIER))
        # self.edges.append(Edge(self.scene, self.nodes[1].outputs[0], self.nodes[2].inputs[2], edge_type=EDGE_TYPE_BEZIER))

    def addNode(self, node):
        self.node.append(node)
        
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


    def cleanupResources(self):
        print("QUITTING")
        try:
            self.scene.glslThread.join()
            # Close the shared memory
            self.scene.shared_mem.close()
            # Unlink (delete) the shared memory
            self.scene.shared_mem.unlink()
        except:
            pass
        




    # def compile(self):
    #     for node in self.nodes:
    #         node.inputNodes = [[], [], [], []]
    #         node.outputNodes = []
    #     print(self.edges)
    #     for edge in self.edges:
    #         if edge.start_socket.input == False: # output to input
    #             edge.start_socket.node.outputNodes.append(edge.end_socket.node)
    #             edge.end_socket.node.inputNodes[edge.end_socket.index].append(edge.start_socket.node)
    #             print(edge.end_socket.node)
    #         else: # input to output
    #             edge.start_socket.node.inputNodes[edge.start_socket.index].append(edge.end_socket.node)
    #             edge.end_socket.node.outputNodes.append(edge.start_socket.node)
    #             print(edge.end_socket.node)
    #     for node in self.nodes:
    #         print("Inputs", node.inputNodes)
    #         print("Outputs", node.outputNodes)
