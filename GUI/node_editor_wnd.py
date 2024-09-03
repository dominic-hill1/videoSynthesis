from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from node_scene import Scene
from node_node import *
from node_edge import Edge, EDGE_TYPE_BEZIER
from node_graphics_view import QDMGraphicsView
from node_sidebar import Sidebar


class NodeEditorWnd(QWidget):
    """
    A class to represent the application window.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stylesheet_filename = 'qss/nodestyle.qss'
        self.loadStylesheet(self.stylesheet_filename)
    
        self.nodes = []
        self.edges = []

        self.initUI()


    def initUI(self):
        """
        Initialise the application window
        """
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # Create graphics scene
        self.scene = Scene()
        self.sidebar = Sidebar(self)

        self.addNodes()

        # Create graphics view
        self.view = QDMGraphicsView(self.scene.grScene, parent=self)
        self.layout.addWidget(self.view)
        self.layout.addWidget(self.sidebar)

        self.setWindowTitle("Video synthesiser")
        self.show()

    def addNodes(self):
        """
        Create initial nodes to be shown on startup
        """
        self.nodes.append(OutputNode(self.scene))
        self.nodes.append(LargeSliderNode(self.scene))
        self.nodes.append(LargeSliderNode(self.scene))
        self.nodes.append(LargeSliderNode(self.scene))
        self.nodes.append(LargeSliderNode(self.scene))
        self.nodes.append(LargeSliderNode(self.scene))
        self.nodes.append(LargeSliderNode(self.scene))
        self.nodes.append(SmallSliderNode(self.scene))
        self.nodes.append(SmallSliderNode(self.scene))
        self.nodes.append(SmallSliderNode(self.scene))
        self.nodes.append(SmallSliderNode(self.scene))
        self.nodes.append(SmallSliderNode(self.scene))
        self.nodes.append(SmallSliderNode(self.scene))

        for node in self.nodes:
            node.setPos(-350, -250)
        self.nodes[0].setPos(350, 250)

    def addNode(self, node):
        """
        Add a node to the window
        """
        self.nodes.append(node)

    def loadStylesheet(self, filename):
        print("Style loading:", filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))


    def cleanupResources(self):
        """
        Cleans up resources after application is quit
        """
        print("QUITTING")
        try:
            self.scene.glslThread.join()
            # Close the shared memory
            self.scene.shared_mem.close()
            # Delete the shared memory
            self.scene.shared_mem.unlink()
        except:
            pass
        