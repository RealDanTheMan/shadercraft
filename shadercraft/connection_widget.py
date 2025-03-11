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

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        """Draws the entire widget"""
        assertRef(self.start)
        assertRef(self.end)

        pen = QPen(Qt.green)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Define control points for the bezier curve.
        p1: QPointF = QPointF(self.start.x() + self.end.x() * 0.5, self.start.y())
        p2: QPointF = QPointF(self.start.x() + self.end.x() * 0.5, self.end.y())

        # Draw cubic smoothed bezier curve between two points.
        path: QPainterPath = QPainterPath()
        path.moveTo(self.start)
        path.cubicTo(p1, p2, self.end)

        painter.drawPath(path)

    def boundingRect(self) -> QRectF:
        """Get bounding box of this widget"""
        assertRef(self.start)
        assertRef(self.end)

        left = min(self.start.x(), self.end.x())
        right = max(self.start.x(), self.end.x())
        top = min(self.start.y(), self.end.y())
        bottom = max(self.start.y(), self.end.y())
        exp = self.pin_radius * 2

        return QRectF(QPointF(left - exp, top - exp), QPointF(right + exp, bottom + exp))

    def updateConnectionPoints(self, a: QPointF, b: QPointF) -> None:
        """
        Update end points of this connection widget.
        Will trigger widger re-draw.
        """
        assertRef(a)
        assertRef(b)

        self.start = a
        self.end = b
        self.prepareGeometryChange()
        self.update()
