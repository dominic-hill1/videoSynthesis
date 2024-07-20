from collections import OrderedDict
from PyQt5.QtWidgets import *
from node_serializable import Serializable
from PyQt5.QtCore import *

from node_socket import LEFT_TOP, LEFT_BOTTOM, RIGHT_TOP, RIGHT_BOTTOM


class QDMNodeContentWidget(QWidget, Serializable):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node

        self.initUI()


#     def initUI(self):
#         self.layout = QVBoxLayout()
#         self.setContentsMargins(0, 0, 0, 0)
#         self.setLayout(self.layout)

#         self.wdg_label = QLabel("Some title")
#         self.layout.addWidget(self.wdg_label)
#         self.layout.addWidget(QDMTextEdit("foo"))



    def serialize(self):
        return OrderedDict([
            
        ])

    def deserialize(self):
        return False


# class QDMTextEdit(QTextEdit):
    
#     def focusInEvent(self, event):
#         print("Focus in")
#         self.parentWidget().setEditingFlag(True)
#         super().focusInEvent(event)

#     def focusOutEvent(self, event):
#         print("Focus out")
#         self.parentWidget().setEditingFlag(False)
#         super().focusOutEvent(event)

class QDMNodeContentOsc(QDMNodeContentWidget):
    def initUI(self):
        self.setContentsMargins(0, 0, 0, 0)

        self.amp_label = QLabel("Amplitude", self)
        self.amp_label.move(5, 50)
        self.rate_label = QLabel("Rate", self)
        self.rate_label.move(5, 88)
        self.freq_label = QLabel("Frequency", self)
        self.freq_label.move(5, 126)

        self.out_label = QLabel("Output", self)
        self.out_label.move(110, 13)

    
class QDMNodeContentColorMixer(QDMNodeContentWidget):

    def initUI(self):
        self.setContentsMargins(0, 0, 0, 0)

        self.red_label = QLabel("Red", self)
        self.red_label.move(5, 10)
        self.green_label = QLabel("Green", self)
        self.green_label.move(5, 50)
        self.blue_label = QLabel("Blue", self)
        self.blue_label.move(5, 90)

        self.out_label = QLabel("Output", self)
        self.out_label.move(110, 130)

class QDMNodeContentColorAdd(QDMNodeContentWidget):

    def initUI(self):
        self.setContentsMargins(0, 0, 0, 0)

        self.red_label = QLabel("Color 1", self)
        self.red_label.move(5, 10)
        self.green_label = QLabel("Color 2", self)
        self.green_label.move(5, 50)

        self.out_label = QLabel("Output", self)
        self.out_label.move(110, 85)

class QDMNodeContentSlider(QDMNodeContentWidget):
    def initUI(self):
        layout = QVBoxLayout()

        # Create a label to display the slider value
        self.label = QLabel("Value: 0", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Create a slider
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)

        self.slider.valueChanged.connect(self.update_label)
        layout.addWidget(self.slider)

        self.setLayout(layout)

    def update_label(self, value):
        self.node.value = value
        self.label.setText(f"Value: {value}")