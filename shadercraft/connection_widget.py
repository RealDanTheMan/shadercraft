from __future__ import annotations
from uuid import UUID, uuid1

from PySide6.QtCore import QObject, QRectF, QPointF, QLine, Qt
from PySide6.QtWidgets import QGraphicsWidget, QWidget, QStyleOptionGraphicsItem
from PySide6.QtGui import QPainter, QPen, QPainterPath

from .asserts import assertRef, assertType
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
        assertType(start, QPointF)
        assertType(end, QPointF)

        self.uuid = uuid
        self.pen: QPen = QPen(Qt.green)
        self.pen.setWidth(3)
        self.__path: QPainterPath = QPainterPath()
        self.__bounds: QRectF = QRectF(QPointF(0.0, 0.0), QPointF(1.0, 1.0))

        self.setZValue(self.depth_order)
        self.updateConnectionPoints(start, end)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        """
        Draw connection widget.
        Draw call is triggered automatically by QT, users should use update instead.

        """
        assertRef(self.pen)
        assertRef(self.__path)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(self.pen)
        painter.drawPath(self.__path)
        painter.setPen(Qt.NoPen)

    def boundingRect(self) -> QRectF:
        """
        Get bounding box of this widget.

        """
        return self.__bounds

    def updateConnectionPoints(self, start: QPointF, end: QPointF) -> None:
        """
        Update connection bezier path based on start and end points.
        Will trigger widger re-draw.

        Parameters:
            a (QPointF) : Connection start point.
            b (QPointF) : Connection end point.

        """
        assertType(start, QPointF)
        assertType(end, QPointF)

        # Derive bezier control points & build cubic path
        p1: QPointF = QPointF(start.x() + end.x() * 0.5, start.y())
        p2: QPointF = QPointF(start.x() + end.x() * 0.5, end.y())

        self.__path.clear()
        self.__path.moveTo(start)
        self.__path.cubicTo(p1, p2, end)

        # Update bounds of this widget.
        self.prepareGeometryChange()
        self.__bounds = QRectF(self.__path.boundingRect())
        self.update()
