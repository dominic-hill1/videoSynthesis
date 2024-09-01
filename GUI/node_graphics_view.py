from PyQt5.QtWidgets import QGraphicsView, QApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_graphics_socket import QDMGraphicsSocket
from node_graphics_edge import QDMGraphicsEdge
from node_edge import Edge, EDGE_TYPE_BEZIER
from node_graphics_cutline import QDMCutLine

MODE_NOOP = 1
MODE_EDGE_DRAG = 2
MODE_EDGE_CUT = 3

EDGE_DRAG_START_THRESHOLD = 10

DEBUG = True

class QDMGraphicsView(QGraphicsView):
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
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)
    
    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)


    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)

    def leftMouseButtonPress(self, event):
        
        item = self.getItemAtClick(event)
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())
        if DEBUG: print("LMB click on: ", item, self.debug_modifiers(event))
         
        # Logic
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers() | Qt.ControlModifier)
                super().mousePressEvent(fakeEvent)
                return
        if type(item) is QDMGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return
            
        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return


        if item is None:
            if event.modifiers() & Qt.ControlModifier:
                self.mode = MODE_EDGE_CUT
                fakeEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.LeftButton, Qt.NoButton, event.modifiers())
                super().mouseReleaseEvent(fakeEvent)
                QApplication.setOverrideCursor(Qt.CrossCursor)
                return

        super().mousePressEvent(event)



    def leftMouseButtonRelease(self, event):
        # Get item which we clicked on
        item = self.getItemAtClick(event)
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                if DEBUG: print("LMB release + Shift on", item)
                event.ignore()
                fakeEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.LeftButton, Qt.NoButton, event.modifiers() | Qt.ControlModifier)
                super().mouseReleaseEvent(fakeEvent)
                return
        if self.mode == MODE_EDGE_DRAG:
            if self.distanceBetweenClickAndReleaseIsOff(event):
                res = self.edgeDragEnd(item)
                if res: return
            
        if self.mode == MODE_EDGE_CUT:
            self.cutIntersectingEdges()
            self.cutline.line_points = []
            self.cutline.update()
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.mode = MODE_NOOP
            return

        super().mouseReleaseEvent(event)
    
    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)

        item = self.getItemAtClick(event)

        # if DEBUG:
        #     if isinstance(item, QDMGraphicsEdge): print("RMB DEBUG:", item.edge, "   Connecting sockets:", item.edge.start_socket, "<-->", item.edge.end_socket)
        #     if type(item) is QDMGraphicsSocket: print("RMB DEBUG:", item.socket, 'has edge:', item.socket.edge)

        #     if item is None:
        #         print("SCENE:")
        #         print("  Nodes:")
        #         for node in self.grScene.scene.nodes: print('    ', node)
        #         print("  Edges:")
        #         for edge in self.grScene.scene.edges: print('    ', edge)
    
    def rightMouseButtonRelease(self, event):
        return super().mouseReleaseEvent(event)
    
    def mouseMoveEvent(self, event):
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragEdge.grEdge.setDestination(pos.x(), pos.y())
            self.dragEdge.grEdge.update()

        if self.mode == MODE_EDGE_CUT:
            pos = self.mapToScene(event.pos())
            self.cutline.line_points.append(pos)
            self.cutline.update()

        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            if not self.editingFlag:
                self.deleteSelected()
            else:
                super().keyPressEvent(event)
        elif event.key() == Qt.Key_S and event.modifiers() & Qt.ControlModifier:
            self.grScene.scene.saveToFile("graph.json.txt")
            self.grScene.scene.compile()

        elif event.key() == Qt.Key_L and event.modifiers() & Qt.ControlModifier:
            self.grScene.scene.loadFromFile("graph.json.txt")
        else:
            super().keyPressEvent(event)

    def cutIntersectingEdges(self):
        
        for ix in range(len(self.cutline.line_points) - 1):
            p1 = self.cutline.line_points[ix]
            p2 = self.cutline.line_points[ix + 1]
            for edge in self.grScene.scene.edges:
                if edge.grEdge.intersectsWith(p1, p2):
                    edge.remove()

    def deleteSelected(self):
        for item in self.grScene.selectedItems():
            if isinstance(item, QDMGraphicsEdge):
                item.edge.remove()
            elif hasattr(item, "node"):
                item.node.remove()

    
    def debug_modifiers(self,event):
        out = "MODS: "
        if event.modifiers() & Qt.ShiftModifier: out += "SHIFT "
        if event.modifiers() & Qt.ControlModifier: out += "CTRL "
        if event.modifiers() & Qt.AltModifier: out += "ALT "
        return out
    
    def getItemAtClick(self, event):
        """Get object on which we have clicked/released mouse button"""
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj
    
    def edgeDragStart(self, item):
        if DEBUG: print("Start dragging edge")
        if DEBUG: print("Assign start socket to: ", item.socket)
        # self.previousEdge = item.socket.edge
        self.last_start_socket = item.socket
        self.dragEdge = Edge(self.grScene.scene, item.socket, None, EDGE_TYPE_BEZIER)
        if DEBUG: print("View::edgeDragStart  ~ dragEdge:", self.dragEdge)

    
    def edgeDragEnd(self, item):
        """Return true to skip rest of code"""
        self.mode = MODE_NOOP
        print("End dragging edge")

        if type(item) is QDMGraphicsSocket:
            if item.socket != self.last_start_socket:
                # if DEBUG: print("View::edgeDragEnd ~ previous edge:", self.previousEdge)
                if item.socket.hasEdge():
                    # item.socket.edge.remove()
                    pass
                if DEBUG: print("View::edgeDragEnd ~ Assign end socket", item.socket)
                # if self.previousEdge is not None: self.previousEdge.remove()
                if DEBUG: print("View::edgeDragEnd ~ Previous edge removed")
                self.dragEdge.start_socket = self.last_start_socket
                self.dragEdge.end_socket = item.socket
                self.dragEdge.start_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.end_socket.setConnectedEdge(self.dragEdge)
                if DEBUG: print("View::edgeDragEnd ~ Assigned start and end sockets to dragEdge")
                self.dragEdge.updatePositions()


                # if self.dragEdge.start_socket.input == False: # output to input
                #     self.dragEdge.start_socket.node.outputNodes.append(self.dragEdge.end_socket.node)
                #     self.dragEdge.end_socket.node.inputNodes[self.dragEdge.end_socket.index].append(self.dragEdge.start_socket.node)
                # else: # input to output
                #     self.dragEdge.start_socket.node.inputNodes[self.dragEdge.start_socket.index].append(self.dragEdge.end_socket.node)
                #     self.dragEdge.end_socket.node.outputNodes.append(self.dragEdge.start_socket.node)
                    
                
                return True
        
        if DEBUG: print("View::edgeDragEnd - End Dragging edge")
        self.dragEdge.remove()
        self.dragEdge = None
        # if DEBUG: print("View::edgeDragEnd ~ about to set socket to previous edge: ", self.previousEdge)
        # if self.previousEdge is not None:
        #     self.previousEdge.start_socket.edge = self.previousEdge
        if DEBUG: print("View: edgeDragEnd - Everything done")
        return False
    
    def distanceBetweenClickAndReleaseIsOff(self, event):
        """Measures if mouse is too close to last LMB click position"""
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        return dist_scene.x() * dist_scene.x() + dist_scene.y() * dist_scene.y() > EDGE_DRAG_START_THRESHOLD*EDGE_DRAG_START_THRESHOLD
    
    def wheelEvent(self, event):
        # Calculate zoom factor
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
    

