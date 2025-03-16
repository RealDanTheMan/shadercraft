from __future__ import annotations
from uuid import UUID, uuid1

from PySide6.QtCore import QObject, QRectF, QPointF, QLine, Qt
from PySide6.QtWidgets import QGraphicsWidget, QWidget
from PySide6.QtGui import QPainter, QPen, QPainterPath

from .asserts import assertRef
from .node_widget import NodeProxyWidget


class ConnectionWidget(QGraphicsWidget):
    """
    Class encapsulates widget representation of node connection.
    Connection is represented by a line connecting two pins between two different nodes.
    """
    pin_radius: float = 6
    depth_order: int = NodeProxyWidget.depth_order - 10

    def __init__(self, uuid: UUID, start: QPointF, end: QPointF) -> None:
        super().__init__()
        assertRef(uuid)
        assertRef(start)
        assertRef(end)

        self.uuid = uuid
        self.start: QPointF = start
        self.end: QPointF = end
        self.setZValue(self.depth_order)
        self.bounds: QRectF = QRectF(QPointF(0.0, 0.0), QPointF(1.0, 1.0))
        self.pen: QPen = QPen(Qt.green)
        self.pen.setWidth(3)
        self.__path: QPainterPath = QPainterPath()
        self.updateConnectionPoints(self.start, self.end)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        """Draws the entire widget"""
        assertRef(self.pen)
        assertRef(self.__path)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(self.pen)
        painter.drawPath(self.__path)
        painter.setPen(Qt.NoPen)

    def boundingRect(self) -> QRectF:
        """Get bounding box of this widget"""
        return self.bounds

    def updateConnectionPoints(self, a: QPointF, b: QPointF) -> None:
        """
        Update end points of this connection widget.
        Will trigger widger re-draw.

        """
        assertRef(a)
        assertRef(b)

        self.start = a
        self.end = b

        # bezier control points.
        p1: QPointF = QPointF(self.start.x() + self.end.x() * 0.5, self.start.y())
        p2: QPointF = QPointF(self.start.x() + self.end.x() * 0.5, self.end.y())

        self.__path.clear()
        self.__path.moveTo(self.start)
        self.__path.cubicTo(p1, p2, self.end)

        self.prepareGeometryChange()
        self.bounds = QRectF(self.__path.boundingRect())
        self.update()
