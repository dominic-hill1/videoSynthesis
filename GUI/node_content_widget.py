from collections import OrderedDict
from PyQt5.QtWidgets import *
from node_serializable import Serializable


class QDMNodeContentWidget(QWidget, Serializable):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node

        self.initUI()


    def initUI(self):
        self.layout = QVBoxLayout()
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.wdg_label = QLabel("Some title")
        self.layout.addWidget(self.wdg_label)
        self.layout.addWidget(QDMTextEdit("foo"))

    def setEditingFlag(self, value):
        self.node.scene.grScene.views()[0].editingFlag = value

    def serialize(self):
        return OrderedDict([
            
        ])

    def deserialize(self):
        return False


class QDMTextEdit(QTextEdit):
    
    def focusInEvent(self, event):
        print("Focus in")
        self.parentWidget().setEditingFlag(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        print("Focus out")
        self.parentWidget().setEditingFlag(False)
        super().focusOutEvent(event)

    
