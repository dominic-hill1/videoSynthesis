from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_node import *


class Sidebar(QWidget):
    def __init__(self, editor, parent=None):
        super().__init__(parent)
        self.editor = editor
        
        # Set up the layout for the sidebar
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setFixedWidth(200)
        
        # Add widgets to the sidebar
        self.button1 = QPushButton('Sin oscillator')
        self.button2 = QPushButton('Square oscillator')
        self.button20 = QPushButton('Circle oscillator')
        self.button3 = QPushButton('Colour Mixer')
        self.button4 = QPushButton('Colour Addition')
        self.button5 = QPushButton('Colour Multiplication')
        self.button6 = QPushButton('Colour Displacement')
        self.button7 = QPushButton('Luma Keying')
        self.button8 = QPushButton('Zooming feedback')
        self.button9 = QPushButton('Variable slider 0-1')
        self.button10 = QPushButton('Variable slider 0-100')
        self.button11 = QPushButton('X-Coordinate')
        self.button12 = QPushButton('Y-Coordinate')        
        self.button13 = QPushButton('Time')        
        self.button14 = QPushButton('Addition')        
        self.button15 = QPushButton('Multiplication')
        self.button16 = QPushButton('Division')
        self.button17 = QPushButton('Negation')
        self.button18 = QPushButton('Video input')
        self.button19 = QPushButton('Audio input')
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button20)
        self.layout.addWidget(self.button18)
        self.layout.addWidget(self.button19)
        self.layout.addWidget(self.button3)
        self.layout.addWidget(self.button4)
        self.layout.addWidget(self.button5)
        self.layout.addWidget(self.button6)
        self.layout.addWidget(self.button7)
        self.layout.addWidget(self.button8)
        self.layout.addWidget(self.button9)
        self.layout.addWidget(self.button10)
        self.layout.addWidget(self.button11)
        self.layout.addWidget(self.button12)
        self.layout.addWidget(self.button13)
        self.layout.addWidget(self.button14)
        self.layout.addWidget(self.button15)
        self.layout.addWidget(self.button16)
        self.layout.addWidget(self.button17)
        
        self.button1.clicked.connect(lambda: self.editor.addNode(SinOscNode(self.editor.scene)))
        self.button2.clicked.connect(lambda: self.editor.addNode(SquareOscNode(self.editor.scene)))
        self.button20.clicked.connect(lambda: self.editor.addNode(CircleOscNode(self.editor.scene)))
        self.button3.clicked.connect(lambda: self.editor.addNode(ColorMixerNode(self.editor.scene)))
        self.button4.clicked.connect(lambda: self.editor.addNode(ColorAddNode(self.editor.scene)))
        self.button5.clicked.connect(lambda: self.editor.addNode(ColorMultNode(self.editor.scene)))
        self.button6.clicked.connect(lambda: self.editor.addNode(ColorDisplaceNode(self.editor.scene)))
        self.button7.clicked.connect(lambda: self.editor.addNode(LumaKeyNode(self.editor.scene)))
        self.button8.clicked.connect(lambda: self.editor.addNode(FeedbackZoomNode(self.editor.scene)))
        self.button9.clicked.connect(lambda: self.editor.addNode(SmallSliderNode(self.editor.scene)))
        self.button10.clicked.connect(lambda: self.editor.addNode(LargeSliderNode(self.editor.scene)))
        self.button11.clicked.connect(lambda: self.editor.addNode(ColorXNode(self.editor.scene)))
        self.button12.clicked.connect(lambda: self.editor.addNode(ColorYNode(self.editor.scene)))
        self.button13.clicked.connect(lambda: self.editor.addNode(TimeNode(self.editor.scene)))
        self.button14.clicked.connect(lambda: self.editor.addNode(AddNode(self.editor.scene)))
        self.button15.clicked.connect(lambda: self.editor.addNode(MultiplyNode(self.editor.scene)))
        self.button16.clicked.connect(lambda: self.editor.addNode(DivideNode(self.editor.scene)))
        self.button17.clicked.connect(lambda: self.editor.addNode(NegateNode(self.editor.scene)))
        self.button18.clicked.connect(lambda: self.editor.addNode(VideoInputNode(self.editor.scene)))
        self.button19.clicked.connect(lambda: self.editor.addNode(AudioNode(self.editor.scene)))





        self.setAttribute(Qt.WA_StyledBackground, True)



