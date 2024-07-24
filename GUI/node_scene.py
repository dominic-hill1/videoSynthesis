import json
from collections import OrderedDict

from node_serializable import Serializable
from node_graphics_scene import QDMGraphicsScene
from node_node import *

class Scene(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        self.scene_width, self.scene_height = 64000, 64000
        self.initUI()

    def initUI(self):
        self.grScene = QDMGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)
    
    def addNode(self, node):
        self.nodes.append(node)
    
    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        self.nodes.remove(node)

    def removeEdge(self, edge):
        self.edges.remove(edge)

    def saveToFile(self, filename):
        with open(filename, "w") as file:
            file.write(json.dumps(self.serialize(), indent=4))
            print("Saving to", filename, "was successful")

    def loadFromFile(self, filename):
        with open(filename, "r") as file:
            raw_data = file.read()
            data = json.loads(raw_data, encoding='utf-8')
            self.deserialize(data)
    
    def serialize(self):
        nodes, edges = [], []
        for node in self.nodes: nodes.append(node.serialize())
        for edge in self.edges: edges.append(edge.serialize())
        return OrderedDict([
            ('id', self.id),
            ('scene_width', self.scene_width),
            ('scene_height', self.scene_height),
            ('nodes', nodes),
            ('edges', edges)
        ])

    def deserialize(self, data, hashmap=[]):
        print("Deserialising")
        return False
    
    def compile(self):
        # Get list of connections for each node
        for node in self.nodes:
            # node.inputNodes = [[], [], [], []]
            node.inputNodes = [None, None, None, None]
            node.outputNodes = []
        print(self.edges)
        for edge in self.edges:
            if edge.start_socket.input == False: # output to input
                edge.start_socket.node.outputNodes.append(edge.end_socket.node)
                # edge.end_socket.node.inputNodes[edge.end_socket.index].append(edge.start_socket.node)
                edge.end_socket.node.inputNodes[edge.end_socket.index] = edge.start_socket.node
                print(edge.end_socket.node)
            else: # input to output
                # edge.start_socket.node.inputNodes[edge.start_socket.index].append(edge.end_socket.node)
                edge.start_socket.node.inputNodes[edge.start_socket.index] = edge.end_socket.node
                edge.end_socket.node.outputNodes.append(edge.start_socket.node)
                print(edge.end_socket.node)
        for node in self.nodes:
            print("Inputs", node.inputNodes)
            print("Outputs", node.outputNodes)

        # Find output node to start algorithm
        for node in self.nodes:
            if isinstance(node, OutputNode):
                output = node
        
        activeNodes = [output]
        code = ""

        while activeNodes != []:
            for node in activeNodes:
                nextWave = []
                for inputNode in node.inputNodes:
                    if inputNode != None:
                        nextWave.append(inputNode)
            print(nextWave)
            activeNodes = nextWave
            
                
            
                





