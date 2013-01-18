from PySide import QtCore, QtGui, QtDeclarative

from fixture import Fixture

class FixtureWidget(QtDeclarative.QDeclarativeItem):

    def __init__(self, parent = None):
        super(FixtureWidget, self).__init__(parent)
        self.setFlag(QtGui.QGraphicsItem.ItemHasNoContents, False)
        self.setAcceptedMouseButtons(QtCore.Qt.MouseButton.LeftButton)
        self.setAcceptsHoverEvents(True)
        self.color = QtGui.QColor(100, 100, 100)
        self.setHeight(16)
        self.setWidth(128)
        self.dragging = False
        self.hovering = False
        self.drag_pos = None
        self.rect = QtCore.QRect(0, 0, 128, 16)

    def paint(self, painter, options, widget):
        if self.hovering:
            painter.setPen(QtGui.QColor(50, 100, 255, 255))
            painter.setBrush(QtGui.QColor(50, 100, 255, 255))
            hover_rect = QtCore.QRect(2, 4, 124, 8)
            painter.drawRoundRect(hover_rect, 16, 16)
        fixture_bg = QtCore.QRect(4, 6, 120, 4)
        painter.fillRect(fixture_bg, QtGui.QColor(200, 200, 0, 200))

    def hoverEnterEvent(self, event):
        self.hovering = True
        self.update()

    def hoverLeaveEvent(self, event):
        self.hovering = False
        self.update()

    def mouseMoveEvent(self, event):
        if self.dragging:
            npos = (event.scenePos() - self.drag_pos)
            self.moveBy(npos.x(), npos.y())
            self.drag_pos = event.scenePos()

    def mousePressEvent(self, event):
        self.dragging = True
        self.drag_pos = event.scenePos()

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.drag_pos = None