from collections import OrderedDict
from node_serializable import Serializable
from node_graphics_node import QDMGraphicsNode
# from node_content_widget import QDMNodeContentWidget
from node_content_widget import QDMNodeContentOsc, QDMNodeContentColorMixer, QDMNodeContentColorAdd, QDMNodeContentSlider
from node_socket import Socket, LEFT_TOP, LEFT_BOTTOM, RIGHT_TOP, RIGHT_BOTTOM

DEBUG = False


class Node(Serializable):
    def __init__(self, scene):
        super().__init__()
        self.scene = scene

        # self.content = QDMNodeContentWidget(self)
        # self.grNode = QDMGraphicsNode(self)

        # self.scene.addNode(self)
        # self.scene.grScene.addItem(self.grNode)

        self.socket_spacing = 40

        self.inputs = []
        self.outputs = []


        # counter = 0
        # for item in inputs:
        #     socket = Socket(node=self, index=counter, position=LEFT_BOTTOM, socket_type=item)
        #     counter += 1
        #     self.inputs.append(socket)

        # counter = 0
        # for item in outputs:
        #     socket = Socket(node=self, index=counter, position=RIGHT_TOP, socket_type=item)
        #     counter += 1
        #     self.outputs.append(socket)


    def __str__(self):
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    @property
    def pos(self):
        return self.grNode.pos()

    def setPos(self, x, y):
        self.grNode.setPos(x, y)

    def getSocketPosition(self, index, position):
        x = 0 if position in (LEFT_TOP, LEFT_BOTTOM) else self.grNode.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            y = self.grNode.height - self.grNode.edge_size - self.grNode._padding - index * self.socket_spacing
        else:
            y = self.grNode.title_height + self.grNode._padding + self.grNode.edge_size + index * self.socket_spacing
        return [x, y]
    
    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()
    
    def remove(self):
        if DEBUG: print("Removing node")
        if DEBUG: print("Removing all edges from sockets")
        for socket in (self.inputs + self.outputs):
            if socket.hasEdge():
                if DEBUG: print("Removing edge from socket")
                socket.edge.remove()
        if DEBUG: print("Removing grNode")
        self.scene.grScene.removeItem(self.grNode)
        if DEBUG: print("Removing node from scene")
        self.scene.removeNode(self)
        if DEBUG: print("All done")
    
    def serialize(self):
        inputs, outputs = [], []
        for socket in self.inputs: inputs.append(socket.serialize())
        for socket in self.outputs: outputs.append(socket.serialize())
        return OrderedDict([
            ('id', self.id),
            ("title", self.title),
            ("pos_x", self.grNode.scenePos().x()),
            ("pos_y", self.grNode.scenePos().y()),
            ("inputs", inputs),
            ("outputs", outputs),
            ("content", self.content.serialize())
        ])

    def deserialize(self, data, hashmap=[]):
        return False

class OscNode(Node):
    def __init__(self, scene):
        super().__init__(scene)

        # self.title = "Sin oscillator"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 200
        self.content = QDMNodeContentOsc(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs.append(Socket(node=self, index=0, position=LEFT_BOTTOM, socket_type=0))
        self.inputs.append(Socket(node=self, index=1, position=LEFT_BOTTOM, socket_type=0))
        self.inputs.append(Socket(node=self, index=2, position=LEFT_BOTTOM, socket_type=0))

        self.outputs.append(Socket(node=self, index=0, position=RIGHT_TOP, socket_type=0))


class SinOscNode(OscNode):
    def __init__(self, scene):
        self.oscType = 0
        self.title = "Sin Oscillator"
        super().__init__(scene)

class SquareOscNode(OscNode):
    def __init__(self, scene):
        self.oscType = 1
        self.title = "Square Oscillator"
        super().__init__(scene)


class ColorMixerNode(Node):
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Colour mixer"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 200
        self.content = QDMNodeContentColorMixer(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs.append(Socket(node=self, index=0, position=LEFT_TOP, socket_type=0))
        self.inputs.append(Socket(node=self, index=1, position=LEFT_TOP, socket_type=0))
        self.inputs.append(Socket(node=self, index=2, position=LEFT_TOP, socket_type=0))

        self.outputs.append(Socket(node=self, index=0, position=RIGHT_BOTTOM, socket_type=0))

    
class ColorAddNode(Node):
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Colour addition"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 160
        self.content = QDMNodeContentColorAdd(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs.append(Socket(node=self, index=0, position=LEFT_TOP, socket_type=0))
        self.inputs.append(Socket(node=self, index=1, position=LEFT_TOP, socket_type=0))

        self.outputs.append(Socket(node=self, index=0, position=RIGHT_BOTTOM, socket_type=0))

class ColorMultNode(Node):
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Colour multiplication"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 160
        self.content = QDMNodeContentColorAdd(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs.append(Socket(node=self, index=0, position=LEFT_TOP, socket_type=0))
        self.inputs.append(Socket(node=self, index=1, position=LEFT_TOP, socket_type=0))

        self.outputs.append(Socket(node=self, index=0, position=RIGHT_BOTTOM, socket_type=0))


class SliderNode(Node):
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Variable input"

        self.value = 0

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 120
        self.content = QDMNodeContentSlider(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)


        self.outputs.append(Socket(node=self, index=0, position=RIGHT_BOTTOM, socket_type=0))