import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_socket import *

EDGE_CP_ROUNDNESS = 100

class QDMGraphicsEdge(QGraphicsPathItem):
    """
    A class to graphically define an edge (line) in the node editor
    """
    def __init__(self, edge, parent=None):
        super().__init__(parent)

        # Define colours, styles, positions
        self.edge = edge
        self._color = QColor("#001000")
        self._color_selected = QColor("#00ff00")
        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)
        self._pen_dragging = QPen(self._color)
        self._pen_dragging.setStyle(Qt.DashLine)
    
        self._pen.setWidthF(2.0)
        self._pen_selected.setWidthF(2.0)
        self._pen_dragging.setWidthF(2.0)
    

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)

        self.posSource = [0, 0]
        self.posDestination = [100, 100]

    def setSource(self, x, y):
        self.posSource = [x, y]
    
    def setDestination(self, x, y):
        self.posDestination = [x, y]


    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # Draw edge
        self.setPath(self.calcPath())

        if self.edge.end_socket is None:
            painter.setPen(self._pen_dragging)
        else:
            painter.setPen(self._pen_selected if self.isSelected() else self._pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def intersectsWith(self, p1, p2):
        cutpath = QPainterPath(p1)
        cutpath.lineTo(p2)
        path = self.calcPath()
        return cutpath.intersects(path)


    def calcPath(self):
        """Will handle drawing QPainterPath from Point A to B"""
        raise NotImplemented("Abstract method must be overriden in child class")
    

class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    """
    A subclass to define an edge with a straight line
    """
    def calcPath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        return path


class QDMGraphicsEdgeBezier(QDMGraphicsEdge):
    """
    A subclass to define an edge with a curved line
    """
    def calcPath(self):
        # Calculate maths for bezier curve. 
        # Credit to Pavel Křupala for this code
        s = self.posSource
        d = self.posDestination

        dist = (d[0] - s[0]) * 0.5

        cpx_s = +dist
        cpx_d = -dist
        cpy_s = 0
        cpy_d = 0

        sspos = self.edge.start_socket.position

        if(s[0] > d[0] and sspos in (RIGHT_TOP, RIGHT_BOTTOM)) or (s[0] < d[0] and sspos in (LEFT_BOTTOM, LEFT_TOP)):
            cpx_d *= -1
            cpx_s *= -1

            cpy_d = (
                (s[1] - d[1]) / math.fabs(
                    (s[1] - d[1]) if (s[1] - d[1] != 0) else 0.000001
                )
            ) * EDGE_CP_ROUNDNESS

            cpy_s = (
                (d[1] - s[1]) / math.fabs(
                    (d[1] - s[1]) if (d[1] - s[1] != 0) else 0.000001
                )
            ) * EDGE_CP_ROUNDNESS

        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo(s[0] + cpx_s, s[1] + cpy_s, d[0] + cpx_d, d[1] + cpy_d, self.posDestination[0], self.posDestination[1])
        return path