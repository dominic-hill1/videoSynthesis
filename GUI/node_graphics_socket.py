from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, socket, socket_type=0):
        self.socket = socket
        super().__init__(socket.node.grNode)

        self.radius = 6
        self.outline_width = 1.0
        self._colors = [
            QColor("#FFFF7700"),
            QColor("#FFFF0000"),
            QColor("#FF00FF00"),
            QColor("#FF0000FF"),
            QColor("#FF52e220"),
            QColor("#FF0056A6") ,
            QColor("#FFA86DB1"),
            QColor("#FFB54747"),
            QColor("#FFDBE220"),

        ]
        self._color_background = self._colors[socket_type]
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
    

