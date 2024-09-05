from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

FLOAT_TYPE = 0
COLOR_TYPE = 1
FEEDBACK_TYPE = 2


class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, socket, socket_type=FLOAT_TYPE):
        """
        A class to graphically define a socket (inputs and outputs to nodes)
        """
        self.socket = socket
        super().__init__(socket.node.grNode)

        self.radius = 6
        self.outline_width = 1.0

        if socket_type == FLOAT_TYPE:
            self._color_background = QColor("#FFFF7700")
        elif socket_type == COLOR_TYPE:
            self._color_background = QColor("#ED254E")
        else: 
            self._color_background = QColor("#48A9A6")

        self._color_outline = QColor("FF000000")

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QBrush(self._color_background)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # Paint circle
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(-self.radius, -self.radius, 2*self.radius, 2 * self.radius)

    def boundingRect(self):
        return QRectF(
            - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width)
        )
    

