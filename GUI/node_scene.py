import json
from collections import OrderedDict
from multiprocessing import shared_memory
import numpy as np

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
        self.shm_name = self.init_comms()

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

    def init_comms(self):
        # Create a shared memory block
        shm = shared_memory.SharedMemory(create=True, size=1024)
        print("Shared memory name:", shm.name)

        with open("../bin/data/shm_name.txt", "w") as file:
            file.write(shm.name)

        return shm.name
        # # Write a string to shared memory
        # message = "Hello from Python"
        # buffer[:len(message)] = message.encode('utf-8')
    
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
            nextWave = []
            for node in activeNodes:
                for inputNode in node.inputNodes:
                    if inputNode != None:
                        nextWave.append(inputNode)
                code = node.writeCode() + "\n" + code
            print(nextWave)
            activeNodes = nextWave


        for node in self.nodes:
            code = node.writeInitCode() + "\n" + code

        print(code)

        with open('frag_template.txt', 'r') as file:
            content = file.read()
            code = content + code + "}"
            code = self.init_shader_vars() + code
            
        
        frag_path = "../bin/data/shadersES2/shader1.frag"
        
        with open(frag_path, "w") as file:
            file.write(code)

        
        
        self.init_cpp()
        self.init_shader_vars()
    
    def init_cpp(self):
        initCode = ""
        variableCode = ""
        ifStatements = ""
        for node in self.nodes:
            if isinstance(node, SliderNode):
                initCode += f"float {node.id} = 0;"
                ifStatements += "if (varName == " + '"' + node.id + '"' + "){" + node.id + "= varValue;}"
                variableCode += 'shader1.setUniform1f("' + node.id + '", ' + node.id + ');\n'
                variableCode += f"std::cout << {node.id} << std::endl;"

        with open("cpp_template.txt", 'r') as file:
            content = file.read()
            content = content.replace("// INSTANTIATE VARIABLES HERE", initCode)
            content = content.replace("// IF STATEMENTS HERE", ifStatements)
            content = content.replace("// SET VARIABLES HERE", variableCode)
            content = content.replace("SHM_NAME", ('"' + self.shm_name + '"'))
                
        with open("../src/ofApp.cpp", "w") as file:
            file.write(content)
        
    def init_shader_vars(self):
        ret = "OF_GLSL_SHADER_HEADER\n"
        for node in self.nodes:
            if isinstance(node, SliderNode):
                ret += f"uniform float {node.id};\n"

        return ret










                
            
                





