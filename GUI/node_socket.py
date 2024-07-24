from collections import OrderedDict
from node_graphics_socket import QDMGraphicsSocket
from node_serializable import Serializable

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4

FLOAT_TYPE = 0
COLOR_TYPE = 1
FEEDBACK_TYPE = 2

class Socket(Serializable):
    def __init__(self, node, input=True, index=0, position=LEFT_TOP, socket_type=0):
        super().__init__()
        self.input = input
        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type


        self.grSocket = QDMGraphicsSocket(self, self.socket_type)
        self.grSocket.setPos(*self.node.getSocketPosition(index, position))

        self.edge = None

    
    def __str__(self):
        return "<Socket %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    def getSocketPosition(self):
        return self.node.getSocketPosition(self.index, self.position)

    def setConnectedEdge(self, edge=None):
        self.edge = edge

    def hasEdge(self):
        return self.edge is not None
    

    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('index', self.index),
            ('position', self.position),
            ('socket_type', self.socket_type)
        ])

    def deserialize(self, data, hashmap=[]):
        return False