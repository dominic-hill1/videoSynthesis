from collections import OrderedDict
from PyQt5.QtWidgets import *
from node_serializable import Serializable
from PyQt5.QtCore import *


class QDMNodeContentWidget(QWidget, Serializable):
    """
    A class to represent the content held within a node.
    This class defines how the middle area of each node will behave
    """
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.initUI()


    def serialize(self):
        return OrderedDict([   
        ])

    def deserialize(self):
        return False


class QDMNodeContentOsc(QDMNodeContentWidget):
    """
    Set labels for sin and square oscillators
    """
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
    """
    Set labels for circle oscillators
    """
    def initUI(self):
        self.setContentsMargins(0, 0, 0, 0)

        self.red_label = QLabel("Amplitude", self)
        self.red_label.move(5, 10)
        self.green_label = QLabel("Frequency", self)
        self.green_label.move(5, 50)

        self.out_label = QLabel("Output", self)
        self.out_label.move(110, 85)

    
class QDMNodeContentColorMixer(QDMNodeContentWidget):
    """
    Set labels for color mixers
    """
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
    """
    Set labels for colour addition modules
    """
    def initUI(self):
        self.setContentsMargins(0, 0, 0, 0)

        self.red_label = QLabel("Color 1", self)
        self.red_label.move(5, 10)
        self.green_label = QLabel("Color 2", self)
        self.green_label.move(5, 50)

        self.out_label = QLabel("Output", self)
        self.out_label.move(110, 85)

class QDMNodeContentLumaKey(QDMNodeContentWidget):
    """
    Set labels for luma keying modules
    """
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
    """
    Set labels for colour displacement modules
    """
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
    """
    Set labels for zooming feedback modules
    """
    def initUI(self):
        self.setContentsMargins(0, 0, 0, 0)

        self.zoom_label = QLabel("Colour", self)
        self.zoom_label.move(5, 10)

        self.zoom_label = QLabel("Zoom factor", self)
        self.zoom_label.move(5, 50)

        self.out_label = QLabel("Output", self)
        self.out_label.move(110, 45)

class QDMNodeContentSliderSmall(QDMNodeContentWidget):
    """
    Set labels and sliders for slider modules
    """
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

        self.slider.valueChanged.connect(self.update)
        layout.addWidget(self.slider)

        self.setLayout(layout)

    def update(self, value):
        """
        Function to be called when slider is moved to update values and labels
        """
        self.node.value = value/1000
        self.node.sendValue()
        self.label.setText("Value: {0:.6g}".format(value/1000))

class QDMNodeContentSliderLarge(QDMNodeContentWidget):
    """
    Set labels and sliders for slider modules
    """
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

        self.slider.valueChanged.connect(self.update)
        layout.addWidget(self.slider)

        self.setLayout(layout)

    def update(self, value):
        """
        Function to be called when slider is moved to update values and labels
        """
        self.node.value = value/100
        self.node.sendValue()
        self.label.setText("Value: {0:.6g}".format(value/100))

class QDMNodeContentColorX(QDMNodeContentWidget):
    """
    Set labels for X-coordinate modules
    """
    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("x-coordinate of pixel", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

class QDMNodeContentColorY(QDMNodeContentWidget):
    """
    Set labels for Y-coordinate modules
    """
    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("y-coordinate of pixel", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)


class QDMNodeContentTime(QDMNodeContentWidget):
    """
    Set labels for time modules
    """
    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("time", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

class QDMNodeContentAudio(QDMNodeContentWidget):
    """
    Set labels for audio modules
    """
    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("Audio volume", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.label2 = QLabel("normalised 0-1", self)
        self.label2.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label2)
        self.setLayout(layout)

class QDMNodeContentCamera(QDMNodeContentWidget):
    """
    Set labels for camera modules
    """
    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("Webcam input", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)



class QDMNodeContentAdd(QDMNodeContentWidget):
    """
    Set labels for addition modules
    """
    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("Add two signals", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

class QDMNodeContentMultiply(QDMNodeContentWidget):
    """
    Set labels for multiplication modules
    """
    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("Multiply two signals", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)


class QDMNodeContentDivide(QDMNodeContentWidget):
    """
    Set labels for division modules
    """
    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("Divide two signals", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)


class QDMNodeContentNegate(QDMNodeContentWidget):
    """
    Set labels for negation modules
    """
    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("Make input negative", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

class QDMNodeContentOutput(QDMNodeContentWidget):
    """
    Set labels for output modules
    """
    def initUI(self):
        self.setContentsMargins(0, 0, 0, 0)

        self.out_label = QLabel("Output to screen", self)
        self.out_label.move(5, 10)
