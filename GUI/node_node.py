from collections import OrderedDict
import uuid

from node_serializable import Serializable
from node_graphics_node import QDMGraphicsNode
# from node_content_widget import QDMNodeContentWidget
from node_content_widget import * 
from node_socket import Socket, LEFT_TOP, LEFT_BOTTOM, RIGHT_TOP, RIGHT_BOTTOM, FLOAT_TYPE, COLOR_TYPE, FEEDBACK_TYPE

DEBUG = False

class Node(Serializable):
    """
    An abstact class to be used to define nodes.
    Nodes are defined using titles, sockets, content, and code. 

    Each node has "code" that is written when the graph is compiled into GLSL code.
    This code consists of a function call (of that module) with its input nodes as parameters,
    saved to a variable name which is a unique ID for the node. 
    This variable name can then be called by other nodes.
    """
    def __init__(self, scene):
        super().__init__()
        self.scene = scene

        self.socket_spacing = 40

        # Input edges
        self.inputs = []
        self.outputs = []

        self.inputNodes = [None, None, None, None]
        self.outputNodes = []

        self.type = None

        self.id = self.generate_id()


    def generate_id(self):
        """
        Generate a unique ID for each node, which can be used as a variable name in its GLSL code
        """
        unique_id = str(uuid.uuid4()).replace('-', '')
        char_id = ''.join(filter(str.isalpha, unique_id))
        return char_id


    def __str__(self):
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    @property
    def pos(self):
        return self.grNode.pos()

    def setPos(self, x, y):
        self.grNode.setPos(x, y)

    def getSocketPosition(self, index, position):
        """
        Return position of a socket on a node
        """
        x = 0 if position in (LEFT_TOP, LEFT_BOTTOM) else self.grNode.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            y = self.grNode.height - self.grNode.edge_size - self.grNode._padding - index * self.socket_spacing
        else:
            y = self.grNode.title_height + self.grNode._padding + self.grNode.edge_size + index * self.socket_spacing
        return [x, y]
    
    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                for edge in socket.edges:
                    edge.updatePositions()
    
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
        pass

class OscNode(Node):
    """
    Superclass to represent sin and square oscillator nodes
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 200
        self.content = QDMNodeContentOsc(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs.append(Socket(node=self, input=True, index=0, position=LEFT_BOTTOM, socket_type=FLOAT_TYPE))
        self.inputs.append(Socket(node=self, input=True, index=1, position=LEFT_BOTTOM, socket_type=FLOAT_TYPE))
        self.inputs.append(Socket(node=self, input=True, index=2, position=LEFT_BOTTOM, socket_type=FLOAT_TYPE))

        self.outputs.append(Socket(node=self, input=False, index=0, position=RIGHT_TOP, socket_type=FLOAT_TYPE))


class SinOscNode(OscNode):
    """
    Class to represent a sin oscillator node
    """
    def __init__(self, scene):
        self.oscType = 0
        self.title = "Sin Oscillator"
        super().__init__(scene)

    def writeInitCode(self):
        code = f"float {self.id} = 0;"
        return code
    def writeCode(self):
        code = f"{self.id} = oscillator({self.inputNodes[0].id}, {self.inputNodes[1].id}, {self.inputNodes[2].id}, 0);"
        return code

class SquareOscNode(OscNode):
    """
    Class to represent a square oscillator node
    """
    def __init__(self, scene):
        self.oscType = 1
        self.title = "Square Oscillator"
        super().__init__(scene)

    def writeInitCode(self):
        code = f"float {self.id} = 0;"
        return code
    def writeCode(self):
        code = f"{self.id} = oscillator({self.inputNodes[0].id}, {self.inputNodes[1].id}, {self.inputNodes[2].id}, 2);"
        return code
    
class CircleOscNode(Node):
    """
    Class to represent circle oscillator node
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Circular Oscillator"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 160
        self.content = QDMNodeContentCircleOsc(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs.append(Socket(node=self, input=True, index=0, position=LEFT_TOP, socket_type=FLOAT_TYPE))
        self.inputs.append(Socket(node=self, input=True, index=1, position=LEFT_TOP, socket_type=FLOAT_TYPE))
        self.outputs.append(Socket(node=self, input=False, index=0, position=RIGHT_BOTTOM, socket_type=FLOAT_TYPE))

    def writeInitCode(self):
        code = f"float {self.id} = 0;"
        return code
    def writeCode(self):
        code = f"{self.id} = circleOscillator({self.inputNodes[0].id}, {self.inputNodes[1].id});"
        return code


class ColorMixerNode(Node):
    """
    Class to represent a colour mixer node
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Colour mixer"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 200
        self.content = QDMNodeContentColorMixer(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs.append(Socket(node=self, input=True, index=0, position=LEFT_TOP, socket_type=FLOAT_TYPE))
        self.inputs.append(Socket(node=self, input=True, index=1, position=LEFT_TOP, socket_type=FLOAT_TYPE))
        self.inputs.append(Socket(node=self, input=True, index=2, position=LEFT_TOP, socket_type=FLOAT_TYPE))

        self.outputs.append(Socket(node=self, input=False, index=0, position=RIGHT_BOTTOM, socket_type=COLOR_TYPE))

    def writeInitCode(self):
        code = f"vec4 {self.id} = vec4(0, 0, 0, 0);"
        return code
    def writeCode(self):
        code = f"{self.id} = vec4({self.inputNodes[0].id}, {self.inputNodes[1].id}, {self.inputNodes[2].id}, 1.0);"
        return code
    
class ColorAddNode(Node):
    """
    Class to represent a colour addition node
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Colour addition"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 160
        self.content = QDMNodeContentColorAdd(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs.append(Socket(node=self, input=True, index=0, position=LEFT_TOP, socket_type=COLOR_TYPE))
        self.inputs.append(Socket(node=self, input=True, index=1, position=LEFT_TOP, socket_type=COLOR_TYPE))

        self.outputs.append(Socket(node=self, input=False, index=0, position=RIGHT_BOTTOM, socket_type=COLOR_TYPE))

    def writeInitCode(self):
        code = f"vec4 {self.id} = vec4(0, 0, 0, 0);"
        return code
    def writeCode(self):
        code = f"{self.id} = vec4(addColor({self.inputNodes[0].id}, {self.inputNodes[1].id}), 1.0);"
        return code

class ColorMultNode(Node):
    """
    Class to represent a colour multiplication node
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Colour multiplication"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 160
        self.content = QDMNodeContentColorAdd(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs.append(Socket(node=self, input=True, index=0, position=LEFT_TOP, socket_type=COLOR_TYPE))
        self.inputs.append(Socket(node=self, input=True, index=1, position=LEFT_TOP, socket_type=COLOR_TYPE))

        self.outputs.append(Socket(node=self, input=False, index=0, position=RIGHT_BOTTOM, socket_type=COLOR_TYPE))

    def writeInitCode(self):
        code = f"vec4 {self.id} = vec4(0, 0, 0, 0);"
        return code
    def writeCode(self):
        code = f"{self.id} = vec4(multiplyColor({self.inputNodes[0].id}, {self.inputNodes[1].id}), 1.0);"
        return code


class ColorDisplaceNode(Node):
    """
    Class to represent a colour displacement node
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Colour displacer"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 240
        self.content = QDMNodeContentColorDisplace(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs.append(Socket(node=self, input=True, index=0, position=LEFT_TOP, socket_type=COLOR_TYPE))
        self.inputs.append(Socket(node=self, input=True, index=1, position=LEFT_TOP, socket_type=FLOAT_TYPE))
        self.inputs.append(Socket(node=self, input=True, index=2, position=LEFT_TOP, socket_type=FLOAT_TYPE))
        self.inputs.append(Socket(node=self, input=True, index=3, position=LEFT_TOP, socket_type=FLOAT_TYPE))

        self.outputs.append(Socket(node=self, input=False, index=0, position=RIGHT_BOTTOM, socket_type=COLOR_TYPE))

    def writeInitCode(self):
        code = f"vec4 {self.id} = vec4(0, 0, 0, 0);"
        return code
    def writeCode(self):
        code = f"{self.id} = colorDisplaceHsb({self.inputNodes[0].id}, {self.inputNodes[1].id}, {self.inputNodes[2].id}, {self.inputNodes[3].id});"
        return code
    

class LumaKeyNode(Node):
    """
    Class to represent luma keying node
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Luma Keying"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 200
        self.content = QDMNodeContentLumaKey(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs.append(Socket(node=self, input=True, index=0, position=LEFT_BOTTOM, socket_type=FLOAT_TYPE))
        self.inputs.append(Socket(node=self, input=True, index=1, position=LEFT_BOTTOM, socket_type=COLOR_TYPE))
        self.inputs.append(Socket(node=self, input=True, index=2, position=LEFT_BOTTOM, socket_type=COLOR_TYPE))

        self.outputs.append(Socket(node=self, input=False, index=0, position=RIGHT_TOP, socket_type=COLOR_TYPE))

    def writeInitCode(self):
        code = f"vec4 {self.id} = vec4(0, 0, 0, 0);"
        return code
    def writeCode(self):
        code = f"{self.id} = vec4(lumaKey({self.inputNodes[2].id}, {self.inputNodes[1].id}, {self.inputNodes[0].id}), 1.0);"
        return code


class FeedbackZoomNode(Node):
    """
    Class to represent a zooming feedback node
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Zooming feedback"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 120
        self.content = QDMNodeContentFeedbackZoom(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs.append(Socket(node=self, input=True, index=0, position=LEFT_TOP, socket_type=COLOR_TYPE))
        self.inputs.append(Socket(node=self, input=True, index=1, position=LEFT_TOP, socket_type=FLOAT_TYPE))
        self.outputs.append(Socket(node=self, input=False, index=0, position=RIGHT_BOTTOM, socket_type=COLOR_TYPE))

        # TODO: Implement writeCode

    def writeInitCode(self):
        return ""
    def writeCode(self):
        code = f"vec2 {self.id}abc = texCoordVarying;"
        code += f"{self.id}abc = feedbackZoom({self.id}abc, {self.inputNodes[1].id});"
        code += f"vec4 {self.id} = texture(tex0, {self.id}abc);"
        return code


class SliderNode(Node):
    """
    Superclass to represent slider nodes
    """
    def writeInitCode(self):
        return ""
    def writeCode(self):
        return ""
    def sendValue(self):
        """
        Get value from slider and change it to shared memory (to c++ backend)
        """
        string = f"{self.id} {self.value:.10f}"
        self.scene.writeToSharedMemory(string)

class SmallSliderNode(SliderNode):
    """
    Class to represent a 0-1 slider node
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Variable input (0-1)"

        self.value = 0

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 120
        self.content = QDMNodeContentSliderSmall(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.outputs.append(Socket(node=self, input=False, index=0, position=RIGHT_BOTTOM, socket_type=FLOAT_TYPE))


class LargeSliderNode(SliderNode):
    """
    Class to represent a 0-100 slider node
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Variable input (0-100)"

        self.value = 0

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 120
        self.content = QDMNodeContentSliderLarge(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.outputs.append(Socket(node=self, input=False, index=0, position=RIGHT_BOTTOM, socket_type=FLOAT_TYPE))

class ColorXNode(Node):
    """
    Class to represent an x-coordinate node
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "X-Coordinate"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 120
        self.content = QDMNodeContentColorX(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.outputs.append(Socket(node=self, input=False, index=0, position=RIGHT_BOTTOM, socket_type=FLOAT_TYPE))
        self.id = "colorx"

        def writeInitCode(self):
            return ""
        def writeCode(self):
            return ""
        
class ColorYNode(Node):
    """
    Class to represent an y-coordinate node
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Y-Coordinate"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 120
        self.content = QDMNodeContentColorY(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.outputs.append(Socket(node=self, input=False, index=0, position=RIGHT_BOTTOM, socket_type=FLOAT_TYPE))
        self.id = "colory"

    def writeInitCode(self):
        return ""
    def writeCode(self):
        return ""
        
class TimeNode(Node):
    """
    Class to represent a time node
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Time"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 120
        self.content = QDMNodeContentTime(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.outputs.append(Socket(node=self, input=False, index=0, position=RIGHT_BOTTOM, socket_type=FLOAT_TYPE))
        self.id = "time"

    def writeInitCode(self):
        return ""
    def writeCode(self):
        return ""
        
class AudioNode(Node):
    """
    Class to represent an audio node
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Audio"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 120
        self.content = QDMNodeContentAudio(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.outputs.append(Socket(node=self, input=False, index=0, position=RIGHT_BOTTOM, socket_type=FLOAT_TYPE))
        self.id = "audio"

    def writeInitCode(self):
        return ""
    def writeCode(self):
        return ""
    

class VideoInputNode(Node):
    """
    Class to represent a video input node
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Video input"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 120
        self.content = QDMNodeContentVideoInput(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.outputs.append(Socket(node=self, input=False, index=0, position=RIGHT_BOTTOM, socket_type=COLOR_TYPE))

    def writeInitCode(self):
        code = f"vec2 {self.id}abc = texCoordVarying;"
        code += f"vec4 {self.id} = texture(input1, {self.id}abc);"
        return code
    def writeCode(self):
        return ""
    

class AddNode(Node):
    """
    Class to represent an addition node
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Addition"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 120
        self.content = QDMNodeContentAdd(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs.append(Socket(node=self, input=True, index=0, position=LEFT_BOTTOM, socket_type=FLOAT_TYPE))
        self.inputs.append(Socket(node=self, input=True, index=1, position=LEFT_BOTTOM, socket_type=FLOAT_TYPE))

        self.outputs.append(Socket(node=self, input=False, index=0, position=RIGHT_TOP, socket_type=FLOAT_TYPE))

    def writeInitCode(self):
        code = f"float {self.id} = 0;"
        return code
    def writeCode(self):
        code = f"{self.id} = {self.inputNodes[0].id} + {self.inputNodes[1].id};"
        return code
    

class MultiplyNode(Node):
    """
    Class to represent a multiplication node
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Multiplication"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 120
        self.content = QDMNodeContentMultiply(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs.append(Socket(node=self, input=True, index=0, position=LEFT_BOTTOM, socket_type=FLOAT_TYPE))
        self.inputs.append(Socket(node=self, input=True, index=1, position=LEFT_BOTTOM, socket_type=FLOAT_TYPE))

        self.outputs.append(Socket(node=self, input=False, index=0, position=RIGHT_TOP, socket_type=FLOAT_TYPE))

    def writeInitCode(self):
        code = f"float {self.id} = 0;"
        return code
    def writeCode(self):
        code = f"{self.id} = {self.inputNodes[0].id} * {self.inputNodes[1].id};"
        return code
    
class DivideNode(Node):
    """
    Class to represent a division node
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Division"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 120
        self.content = QDMNodeContentDivide(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs.append(Socket(node=self, input=True, index=0, position=LEFT_BOTTOM, socket_type=FLOAT_TYPE))
        self.inputs.append(Socket(node=self, input=True, index=1, position=LEFT_BOTTOM, socket_type=FLOAT_TYPE))

        self.outputs.append(Socket(node=self, input=False, index=0, position=RIGHT_TOP, socket_type=FLOAT_TYPE))

    def writeInitCode(self):
        code = f"float {self.id} = 0;"
        return code
    def writeCode(self):
        code = f"{self.id} = {self.inputNodes[0].id} / {self.inputNodes[1].id};"
        return code
    
class NegateNode(Node):
    """
    Class to represent a negation node
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Negate"

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 120
        self.content = QDMNodeContentNegate(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs.append(Socket(node=self, input=True, index=0, position=LEFT_BOTTOM, socket_type=FLOAT_TYPE))

        self.outputs.append(Socket(node=self, input=False, index=0, position=RIGHT_TOP, socket_type=FLOAT_TYPE))

    def writeInitCode(self):
        code = f"float {self.id} = 0;"
        return code
    def writeCode(self):
        code = f"{self.id} = -{self.inputNodes[0].id};"
        return code

class OutputNode(Node):
    """
    Class to represent an output node
    """
    def __init__(self, scene):
        super().__init__(scene)

        self.title = "Output"

        self.value = 0

        self.grNode = QDMGraphicsNode(self)
        self.grNode.height = 80
        self.content = QDMNodeContentOutput(self)
        self.grNode.initContent()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs.append(Socket(node=self, input=True, index=0, position=LEFT_TOP, socket_type=COLOR_TYPE))

    def writeInitCode(self):
        return ""
    def writeCode(self):
        code = f"outputColor = {self.inputNodes[0].id};"
        return code