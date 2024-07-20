import sys
from PyQt5.QtCore import Qt, QPointF, QRectF, QLineF
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem, QVBoxLayout


class Node(QGraphicsItem):
    def __init__(self):
        super().__init__()
        self.radius = 20
        self.color = QColor(Qt.blue)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.edges = []

    def boundingRect(self):
        adjust = 2.0
        return QRectF(-self.radius - adjust, -self.radius - adjust,
                      2 * self.radius + adjust, 2 * self.radius + adjust)

    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.black, 0))
        painter.setBrush(self.color)
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

    def add_edge(self, edge):
        self.edges.append(edge)

    def edges(self):
        return self.edges


class Edge(QGraphicsItem):
    def __init__(self, source_node, dest_node):
        super().__init__()
        self.source_point = QPointF()
        self.dest_point = QPointF()
        self.source_node = source_node
        self.dest_node = dest_node
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.source_node.add_edge(self)
        self.dest_node.add_edge(self)

    def boundingRect(self):
        return QRectF()

    def paint(self, painter, option, widget):
        line = QLineF(self.mapFromItem(self.source_node, 0, 0),
                      self.mapFromItem(self.dest_node, 0, 0))
        if line.length() == 0.0:
            return

        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(line)

    def type(self):
        return QGraphicsItem.UserType + 2


class NodeEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Node Editor')

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.nodes = []

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            node = Node()
            node.setPos(event.pos())
            self.scene.addItem(node)
            self.nodes.append(node)

            if len(self.nodes) > 1:
                edge = Edge(self.nodes[-2], self.nodes[-1])
                self.scene.addItem(edge)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = NodeEditor()
    editor.show()
    sys.exit(app.exec_())
