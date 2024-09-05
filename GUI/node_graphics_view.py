from PyQt5.QtWidgets import QGraphicsView, QApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_graphics_socket import QDMGraphicsSocket
from node_graphics_edge import QDMGraphicsEdge
from node_edge import Edge, EDGE_TYPE_BEZIER
from node_graphics_cutline import QDMCutLine
from node_node import OutputNode, LargeSliderNode, SmallSliderNode

MODE_NOOP = 1
MODE_EDGE_DRAG = 2
MODE_EDGE_CUT = 3

EDGE_DRAG_START_THRESHOLD = 10

DEBUG = True

class QDMGraphicsView(QGraphicsView):
    """
    A class to define the view of the node editor. 
    Events are handled in this class
    """
    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.editor = parent
        self.grScene = grScene
        self.initUI()
        self.setScene(self.grScene)
        self.mode = MODE_NOOP
        self.editingFlag = False
        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]

        # Cutline
        self.cutline = QDMCutLine()
        self.grScene.addItem(self.cutline)


    def initUI(self):
        # Define general rules
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def mousePressEvent(self, event):
        # Event handling for mouse pressing
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)


    def mouseReleaseEvent(self, event):
        # Event handling for mouse release
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)
    
    def middleMouseButtonPress(self, event):
        # Event handling for middle mouse button press (start drag)
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)


    def middleMouseButtonRelease(self, event):
        # Event handling for middle mouse button release (end drag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)

    def leftMouseButtonPress(self, event):
        # Event handling for left mouse button presed
        item = self.getItemAtClick(event)
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())
         
        # Logic depending on what item is pressed
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None: # If node, edge is pressed, pass event to pyqt5 event handling
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers() | Qt.ControlModifier)
                super().mousePressEvent(fakeEvent)
                return
        if type(item) is QDMGraphicsSocket: # If socket is pressed, start new edge
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return
            
        if self.mode == MODE_EDGE_DRAG: # If edge is already being made, end edge drag
            res = self.edgeDragEnd(item)
            if res: return

        if item is None:
            if event.modifiers() & Qt.ControlModifier: # Cutline
                self.mode = MODE_EDGE_CUT
                fakeEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.LeftButton, Qt.NoButton, event.modifiers())
                super().mouseReleaseEvent(fakeEvent)
                QApplication.setOverrideCursor(Qt.CrossCursor)
                return

        super().mousePressEvent(event)



    def leftMouseButtonRelease(self, event):
        # Handle when left mouse button is released
        item = self.getItemAtClick(event)
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None: # Pass event to pyqt5 event handling
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.LeftButton, Qt.NoButton, event.modifiers() | Qt.ControlModifier)
                super().mouseReleaseEvent(fakeEvent)
                return
        if self.mode == MODE_EDGE_DRAG: # End dragging edge
            if self.distanceBetweenClickAndReleaseIsOff(event):
                res = self.edgeDragEnd(item)
                if res: return
            
        if self.mode == MODE_EDGE_CUT: # Delete edges over cutline
            self.cutIntersectingEdges()
            self.cutline.line_points = []
            self.cutline.update()
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.mode = MODE_NOOP
            return

        super().mouseReleaseEvent(event)
    
    def rightMouseButtonPress(self, event):
        # If right mouse button is pressed, do nothing
        super().mousePressEvent(event)

    
    def rightMouseButtonRelease(self, event):
        # If right mouse button is released, do nothing
        return super().mouseReleaseEvent(event)
    
    def mouseMoveEvent(self, event):
        # Event handling for when mouse is dragged
        if self.mode == MODE_EDGE_DRAG: # If new edge is being created, update edge position
            pos = self.mapToScene(event.pos())
            self.dragEdge.grEdge.setDestination(pos.x(), pos.y())
            self.dragEdge.grEdge.update()

        if self.mode == MODE_EDGE_CUT: # If cutline is being made, update cutline position
            pos = self.mapToScene(event.pos())
            self.cutline.line_points.append(pos)
            self.cutline.update()

        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        # Event handling for key presses
        if event.key() == Qt.Key_Delete: # Delete selected item when delete is pressed
            if not self.editingFlag:
                self.deleteSelected()
            else:
                super().keyPressEvent(event)
        elif event.key() == Qt.Key_S and event.modifiers() & Qt.ControlModifier: # Compile when ctrl-s is pressed
            self.grScene.scene.saveToFile("graph.json.txt")
            self.grScene.scene.compile()

        elif event.key() == Qt.Key_L and event.modifiers() & Qt.ControlModifier: # Not complete yet
            self.grScene.scene.loadFromFile("graph.json.txt")
        else:
            super().keyPressEvent(event)

    def cutIntersectingEdges(self):
        # Find edges cutline intersects with and delete these edges
        for ix in range(len(self.cutline.line_points) - 1):
            p1 = self.cutline.line_points[ix]
            p2 = self.cutline.line_points[ix + 1]
            for edge in self.grScene.scene.edges:
                if edge.grEdge.intersectsWith(p1, p2):
                    edge.remove()

    def deleteSelected(self):
        # Delete selected item if it is not an output or slider node.
        for item in self.grScene.selectedItems():
            if isinstance(item, QDMGraphicsEdge):
                item.edge.remove()
            elif hasattr(item, "node"):
                if not isinstance(item.node, OutputNode):
                    if not isinstance(item.node, SmallSliderNode):
                        if not isinstance(item.node, LargeSliderNode):
                            item.node.remove()

    
    def debug_modifiers(self,event):
        out = "MODS: "
        if event.modifiers() & Qt.ShiftModifier: out += "SHIFT "
        if event.modifiers() & Qt.ControlModifier: out += "CTRL "
        if event.modifiers() & Qt.AltModifier: out += "ALT "
        return out
    
    def getItemAtClick(self, event):
        """Get object clicked/released on with mouse button"""
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj
    
    def edgeDragStart(self, item):
        # Start dragging new edge
        self.last_start_socket = item.socket
        self.dragEdge = Edge(self.grScene.scene, item.socket, None, EDGE_TYPE_BEZIER)


    
    def edgeDragEnd(self, item):
        # End dragging new edge, connect with new socket
        self.mode = MODE_NOOP

        if type(item) is QDMGraphicsSocket:
            if item.socket != self.last_start_socket: # Edge can't go to same socket it came from
                if item.socket.hasEdge():
                    # item.socket.edge.remove()
                    pass
                # Set new socket connection
                self.dragEdge.start_socket = self.last_start_socket
                self.dragEdge.end_socket = item.socket
                self.dragEdge.start_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.end_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.updatePositions()
                return True
        
        self.dragEdge.remove() # Delete temp edge if socket is not valid
        self.dragEdge = None
 
        return False
    
    def distanceBetweenClickAndReleaseIsOff(self, event):
        # Measures if mouse is too close to last LMB click position
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        return dist_scene.x() * dist_scene.x() + dist_scene.y() * dist_scene.y() > EDGE_DRAG_START_THRESHOLD*EDGE_DRAG_START_THRESHOLD
    
    def wheelEvent(self, event):
        # Handle zooming
        zoomOutFactor = 1 / self.zoomInFactor

        # Calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True

        # Set scene scale
        if not clamped or self.zoomClamp == False:
            self.scale(zoomFactor, zoomFactor)
    

