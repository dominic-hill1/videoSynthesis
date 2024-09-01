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

class QDMNodeContentCircleOsc(QDMNodeContentWidget):
    def initUI(self):
        self.setContentsMargins(0, 0, 0, 0)

        self.red_label = QLabel("Amplitude", self)
        self.red_label.move(5, 10)
        self.green_label = QLabel("Frequency", self)
        self.green_label.move(5, 50)

        self.out_label = QLabel("Output", self)
        self.out_label.move(110, 85)

    
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

class QDMNodeContentLumaKey(QDMNodeContentWidget):
    def initUI(self):
        self.setContentsMargins(0, 0, 0, 0)

        self.amp_label = QLabel("Default colour", self)
        self.amp_label.move(5, 50)
        self.rate_label = QLabel("Alternative colour", self)
        self.rate_label.move(5, 88)
        self.freq_label = QLabel("Sensitivity", self)
        self.freq_label.move(5, 126)

        self.out_label = QLabel("Output", self)
        self.out_label.move(110, 13)

    
class QDMNodeContentColorDisplace(QDMNodeContentWidget):
    def initUI(self):
        self.setContentsMargins(0, 0, 0, 0)

        self.color_label = QLabel("Colour", self)
        self.color_label.move(5, 10)
        self.x_label = QLabel("x", self)
        self.x_label.move(5, 48)
        self.y_label = QLabel("y", self)
        self.y_label.move(5, 88)
        self.z_label = QLabel("z", self)
        self.z_label.move(5, 128)

        self.out_label = QLabel("Output", self)
        self.out_label.move(110, 168)

class QDMNodeContentFeedbackZoom(QDMNodeContentWidget):

    def initUI(self):
        self.setContentsMargins(0, 0, 0, 0)

        self.zoom_label = QLabel("Colour", self)
        self.zoom_label.move(5, 10)

        self.zoom_label = QLabel("Zoom factor", self)
        self.zoom_label.move(5, 50)

        self.out_label = QLabel("Output", self)
        self.out_label.move(110, 45)

class QDMNodeContentSliderSmall(QDMNodeContentWidget):
    def initUI(self):
        layout = QVBoxLayout()

        # Create a label to display the slider value
        self.label = QLabel("Value: 0", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Create a slider
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(1000)
        self.slider.setValue(0)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(100)

        self.slider.valueChanged.connect(self.update_label)
        layout.addWidget(self.slider)

        self.setLayout(layout)

    def update_label(self, value):
        self.node.value = value/1000
        self.node.sendValue()
        self.label.setText("Value: {0:.6g}".format(value/1000))

class QDMNodeContentSliderLarge(QDMNodeContentWidget):
    def initUI(self):
        layout = QVBoxLayout()

        # Create a label to display the slider value
        self.label = QLabel("Value: 0", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Create a slider
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(10000)
        self.slider.setValue(0)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1000)

        self.slider.valueChanged.connect(self.update_label)
        layout.addWidget(self.slider)

        self.setLayout(layout)

    def update_label(self, value):
        self.node.value = value/100
        self.node.sendValue()
        self.label.setText("Value: {0:.6g}".format(value/100))

class QDMNodeContentColorX(QDMNodeContentWidget):
    def initUI(self):
        layout = QVBoxLayout()

        # Create a label to display the slider value
        self.label = QLabel("x-coordinate of pixel", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

class QDMNodeContentColorY(QDMNodeContentWidget):
    def initUI(self):
        layout = QVBoxLayout()

        # Create a label to display the slider value
        self.label = QLabel("y-coordinate of pixel", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)


class QDMNodeContentTime(QDMNodeContentWidget):
    def initUI(self):
        layout = QVBoxLayout()

        # Create a label to display the slider value
        self.label = QLabel("time", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

class QDMNodeContentAudio(QDMNodeContentWidget):
    def initUI(self):
        layout = QVBoxLayout()

        # Create a label to display the slider value
        self.label = QLabel("Audio volume", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.label2 = QLabel("normalised 0-1", self)
        self.label2.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label2)
        self.setLayout(layout)

class QDMNodeContentCamera(QDMNodeContentWidget):
    def initUI(self):
        layout = QVBoxLayout()

        # Create a label to display the slider value
        self.label = QLabel("Webcam input", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)



class QDMNodeContentAdd(QDMNodeContentWidget):
    def initUI(self):
        layout = QVBoxLayout()

        # Create a label to display the slider value
        self.label = QLabel("Add two signals", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

class QDMNodeContentMultiply(QDMNodeContentWidget):
    def initUI(self):
        layout = QVBoxLayout()

        # Create a label to display the slider value
        self.label = QLabel("Multiply two signals", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)


class QDMNodeContentDivide(QDMNodeContentWidget):
    def initUI(self):
        layout = QVBoxLayout()

        # Create a label to display the slider value
        self.label = QLabel("Divide two signals", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)


class QDMNodeContentNegate(QDMNodeContentWidget):
    def initUI(self):
        layout = QVBoxLayout()
        # Create a label to display the slider value
        self.label = QLabel("Make input negative", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

class QDMNodeContentOutput(QDMNodeContentWidget):
    def initUI(self):
        self.setContentsMargins(0, 0, 0, 0)

        self.out_label = QLabel("Output to screen", self)
        self.out_label.move(5, 10)


        # self.feedback_label = QLabel("Feedback", self)
        # self.feedback_label.move(5, 50)
