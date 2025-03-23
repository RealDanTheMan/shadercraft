from __future__ import annotations
from typing import Optional
from uuid import UUID, uuid1
import logging as Log

from PySide6.QtWidgets import (
    QGraphicsScene,
    QWidget,
    QGraphicsItem,
    QGraphicsProxyWidget,
    QGraphicsView
)
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Signal, Slot, QObject, QPoint, Qt, QPointF

from .node import Node, NodeConnection, NodeIO, INodeGraphContext
from .node_widget import NodeProxyWidget, NodePinShapeWidget
from .connection_widget import ConnectionWidget
from .shadernodes import FloatShaderNode, MulShaderNode
from .output_shadernodes import PhongOutputShaderNode
from .asserts import assertRef, assertFalse, assertTrue, assertType
from .apputils import NameDeduplicator


class NodeGraphScene(QGraphicsScene, INodeGraphContext):
    """
    Class that represents node graph scene.
    All the nodes and their connections are stored in the scene
    """
    selected_node_changed: Signal = Signal(Node)
    preview_redraw_requested: Signal = Signal()

    def __init__(self):
        """Default constructor"""
        super().__init__()

        self.__name_generator: NameDeduplicator = NameDeduplicator()
        self.__nodes: list[Node] = []
        self.__connections: list[NodeConnection] = []
        self.__names: list[str] = []
        self.__names_lookup: dict[str, int] = {}
        self.__drag_pin: Optional[UUID] = None
        self.__drag_pin_owner: Optional[Node] = None
        self.__drop_pin: Optional[UUID] = None
        self.__drop_pin_owner: Optional[Node] = None
        self.__drag_drop_preview: Optional[ConnectionWidget] = None
        self.__selected_node: Optional[Node] = None

        self.filepath: str = None

    def getView(self) -> Optional[QGraphicsView]:
        """Get handle to the first view which this scene is bound to"""
        if len(self.views()) > 0:
            return self.views()[0]
        return None

    def screenCoordsToScene(self, screen_coords: QPoint) -> QPointF:
        """Get position in scene coordinates from given screen position"""
        assertRef(screen_coords)
        view: QGraphicsView = self.getView()
        assertRef(view)
        local_pos: QPointF = view.mapFromGlobal(screen_coords)
        return view.mapToScene(local_pos)

    def getSelectedNode(self) -> Optional[Node]:
        """Get currently selected node in the graph"""
        return self.__selected_node

    def addNode(self, node: Node) -> None:
        """
        Add node to this node graph.
        Added node will be renamed if needed to ensure name uniquness.
        """
        assertRef(node)
        assertFalse(node in self.__nodes, "Node already present in the scene")
        Log.debug(f"Adding new to the graph -> {node} @ {node.posx}x{node.posy}")

        node.name = self.__name_generator.registerName(node.name)
        if node.getWidget() is None:
            node.initWidget()

        node.bindGraphContext(self)
        self.__nodes.append(node)
        self.addItem(node.getWidget())

        node.selectionChanged.connect(self.onNodeSelectionChanged)
        Log.info(f"NodeGraphScene: Adding new node -> {node.uuid}")

    def deleteNode(self, node: Node) -> None:
        """
        Removes given node from the graph.
        Any connection to or from the node will be removed as well.
        """
        assertTrue(node in self.__nodes, "Node does not exists within the node graph!")
        Log.info(f"Removing node from node graph: '{node.name}' @ {node.uuid}")

        self.__name_generator.deregisterName(node.name)

        # Remove active connections to given node
        in_cons: list[NodeConnection] = self.getNodeDownstreamConnections(node)
        out_cons: list[NodeConnection] = self.getNodeUpstreamConnections(node)

        for con in in_cons + out_cons:
            self.removeNodeConnection(con)

        # Remove the actual node
        self.__nodes.remove(node)
        if node.getWidget() is not None:
            self.removeItem(node.getWidget())

    def deleteAllNodes(self) -> None:
        """
        Removes all nodes and their connections from the active graph scene.
        
        """
        for node in self.getAllNodes():
            self.deleteNode(node)

    def deleteSelectedNode(self) -> bool:
        """Delete currently selected node in the graph scene"""
        node: Optional[Node] = self.getSelectedNode()
        if node is not None:
            self.deleteNode(node)
            return True
        return False

    def addDefaultNodes(self) -> None:
        """Create and add set of node to the scene, usefull for testing"""
        node0 = MulShaderNode()
        node1 = FloatShaderNode()
        node2 = FloatShaderNode()
        node3 = PhongOutputShaderNode()

        self.addNode(node0)
        self.addNode(node1)
        self.addNode(node2)
        self.addNode(node3)

        node0.setPosition(-200.0, 200.0)
        node1.setPosition(300.0, -100.0)
        node2.setPosition(0.0, 0.0)
        node3.setPosition(500.0, 0.0)

    def addNodeConnection(self, connection: NodeConnection) -> None:
        """
        Add node connection to this graph.

        """
        assertRef(connection)
        assertRef(connection.getWidget)

        connection.bindGraphContext(self)
        self.__connections.append(connection)
        self.addItem(connection.getWidget())

    def removeNodeConnection(self, connection: NodeConnection) -> None:
        """
        Removes existing node connection from this node graph scene.

        """
        assertType(connection, NodeConnection)

        # Disconnect the connection from the parent node first.
        connection.getOwnerNode().removeConnection((connection.uuid))
        connection.bindGraphContext(None)

        # Remove the connection from the graph scene.
        self.removeItem(connection.getWidget())
        self.__connections.remove(connection)

    def removeAllNodeConnections(self) -> None:
        """
        Removes all existing node connections from the scene.
        Individual nodes will still retain connection information but it will no longer be
        part of this node graphs scene.

        """
        for connection in self.__connections:
            self.removeItem(connection.getWidget())

        self.__connections.clear()

    def getAllNodes(self) -> list[Node]:
        """Get list of all nodes present in the graph"""
        return list(self.__nodes)

    def getAllNodeOfClass(self, cls) -> list[Node]:
        """Get List of all nodes present in the graph that match given class type"""
        nodes: list[Node] = []
        for node in self.__nodes:
            if isinstance(node, cls):
                nodes.append(node)
        return nodes

    def getNodeFromUUID(self, uuid: UUID) -> Optional[Node]:
        """Get node in the scene that matches given UUID"""
        for node in self.__nodes:
            if node.uuid == uuid:
                return node
        return None

    def getNodeFromWidget(self, widget: NodeProxyWidget) -> Optional[Node]:
        """Get handle to the node linked to given node widget"""

        assertRef(widget)
        match = [node for node in self.__nodes if node.getWidget() is widget]
        if match:
            return match[0]
        return None

    def getNodeFromWidgetUUID(self, uuid: UUID) -> Optional[Node]:
        """Get node linked to widget that matches given widget UUID"""

        assertRef(uuid)
        widget = self.getWidgetFromUUID(uuid)
        if widget:
            return self.getNodeFromWidget(widget)
        return None

    def getWidgetFromUUID(self, uuid: UUID) -> Optional[NodeProxyWidget]:
        """Get node widget matching given UUID"""

        assertRef(uuid)
        match = [node.getWidget() for node in self.__nodes if node.getWidget() and node.getWidget().uuid is uuid]
        assertTrue(len(match) <= 1)
        if match:
            return match[0]
        return None

    def getNodeDownstreamConnections(self, node: Node) -> list[NodeConnection]:
        """Get all incoming connections in the node graph from given node"""
        assertRef(node)
        assertTrue (node in self.__nodes)
        return node.getAllConnections()

    def getNodeUpstreamConnections(self, node: Node) -> list[NodeConnection]:
        """Get all outgoing connections in the node graph to given node"""
        assertRef(node)
        assertTrue(node in self.__nodes)

        connections: list[NodeConnection] = []
        for inode in self.__nodes:
            if inode.uuid is node.uuid:
                continue
            node_connections: list[NodeConnection] = inode.getAllConnections()
            for con in node_connections:
                if con.source is node.uuid:
                    connections.append(con)

        return connections

    def getWidgetUnderMouse(self, scene_pos: QPointF) -> Optional[QWidget]:
        """Get hadle to the windget currently under mouse pointer"""
        item: QGraphicsItem = self.itemAt(scene_pos, self.views()[0].transform())
        if item is not None and isinstance(item, QGraphicsProxyWidget):
            if item.widget() is None:
                return None
            pos: QPoint = item.mapFromScene(scene_pos)
            widget: QWidget = item.widget().childAt(pos)
            return widget
        return None

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Event handler invoked when mouse button press happens inside the graph scene"""
        if event.button() == Qt.MouseButton.LeftButton:
            widget: QWidget = self.getWidgetUnderMouse(event.scenePos())
            if widget is not None and isinstance(widget, NodePinShapeWidget):
                node: Node = self.getNodeFromUUID(widget.node_uuid)
                assertRef(node)
                self.beginPinDragDrop(node, widget.property_uuid)
                return
        self.resetPinDragDrop()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Event handler invoked when mouse button is released inside graph scene"""
        widget: QWidget = self.getWidgetUnderMouse(event.scenePos())
        if widget is not None and isinstance(widget, NodePinShapeWidget):
            node: Node = self.getNodeFromUUID(widget.node_uuid)
            pin_uuid: UUID = widget.property_uuid
            assertRef(node)
            assertRef(pin_uuid)
            if event.button() == Qt.MouseButton.LeftButton:
                self.endPinDragDrop(node, pin_uuid)
                event.accept()
                return

            if event.button() == Qt.MouseButton.RightButton:
                # Disconnect exiting connection on right clicks
                node_input: NodeIO = node.getNodeInput(pin_uuid)
                if node_input is not None:
                    con: NodeConnection = node.getConnectionFromInput(node_input)
                    if con is not None:
                        self.removeNodeConnection(con)
                        event.accept()
                        return

        self.resetPinDragDrop()
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Event handler invoked when the mouse is moved inside the graph scene"""
        start_node: Node = self.__drag_pin_owner
        start_pin: UUID = self.__drag_pin
        if start_node is not None and start_pin is not None:
            start: QPoint = start_node.getWidget().getPinScenePos(start_pin)
            end: QPoint = self.screenCoordsToScene(event.screenPos())
            assertRef(start)
            assertRef(end)
            if self.__drag_drop_preview is None:
                self.__drag_drop_preview = ConnectionWidget(uuid1(), start, end)
                self.addItem(self.__drag_drop_preview)
            else:
                self.__drag_drop_preview.updateConnectionPoints(start, end)
        super().mouseMoveEvent(event)

    def beginPinDragDrop(self, node: Node, pin: UUID) -> None:
        """Start of node pin drag & drop event flow"""
        assertRef(node)
        assertRef(pin)
        Log.debug(f"Node pin drag registered [node:{node}] [pin:{pin}]")

        self.__drag_pin = pin
        self.__drag_pin_owner = node
        self.__drop_pin = None
        self.__drop_pin_owner = None

    def endPinDragDrop(self, node: Node, pin: UUID) -> None:
        """End of node pin drag & drop event flow"""
        assertRef(node)
        assertRef(pin)
        Log.debug(f"Node pin drop registered [node:{node}] [pin:{pin}]")

        self.__drop_pin = pin
        self.__drop_pin_owner = node
        self.finalisePinDragDrop()

    def resetPinDragDrop(self) -> None:
        """Resets node pin drag & drop event flow"""
        self.__drag_pin = None
        self.__drag_pin_owner = None
        self.__drop_pin = None
        self.__drop_pin_owner = None

        if self.__drag_drop_preview is not None:
            self.removeItem(self.__drag_drop_preview)
            self.__drag_drop_preview.setParent(None)
            self.__drag_drop_preview.deleteLater()
            self.__drag_drop_preview = None

    def finalisePinDragDrop(self) -> None:
        """Finalise node pin drag & drop event and create connection if valid"""
        source_node: Node = self.__drag_pin_owner
        source_pin: UUID = self.__drag_pin
        target_node: Node = self.__drop_pin_owner
        target_pin: UUID = self.__drop_pin

        self.resetPinDragDrop()

        if source_node is None or source_pin is None:
            Log.debug("Aborting pin drag & drop: source pin or its owner node are invalid")
            return

        if target_node is None or target_pin is None:
            Log.debug("Aborting pin drag & drop: target pin or its owner node are invalid")
            return

        if source_node.getNodeOutput(source_pin) is None:
            Log.debug("Aborting pin drag & drop: source pin is not of output type")
            return

        if target_node.getNodeInput(target_pin) is None:
            Log.debug("Aborting pin drag & drop: target pin is not of input type")
            return

        if source_node.uuid == target_node.uuid:
            Log.debug("Aborting pin drag & drop: pins share parents")
            return

        self.attemptNodeConnection(source_node, source_pin, target_node, target_pin)

    def attemptNodeConnection(
        self,
        source_node: Node,
        source_pin: UUID,
        target_node: Node,
        target_pin: UUID
    ) -> bool:
        """
        Attempts to connect two node via input/output pins.
        Source side of the connection is output property of a node.
        Target side of the connection is input property of another node.
        """
        assertRef(source_node)
        assertRef(source_pin)
        assertRef(target_node)
        assertRef(target_pin)
        Log.debug(f"Attempting node connection: {source_pin} -> {target_pin}")

        assertTrue(source_node.uuid != target_node, "Attempting to connect node to itself")

        node_in = target_node.getNodeInput(target_pin)
        node_out = source_node.getNodeOutput(source_pin)
        assertRef(node_out, "Source connection has no matching node output")
        assertRef(node_in, "Target connection has no matching node input")

        # Remove existing connection if one is present
        excon: NodeConnection = target_node.getConnectionFromInput(node_in)
        if excon is not None:
            self.removeNodeConnection(excon)

        # Create new connection
        success: bool = target_node.addConnection(source_node, node_in.uuid, node_out.uuid)
        if success:
            self.addNodeConnection(target_node.getConnectionFromInput(node_in))
            self.preview_redraw_requested.emit()

        return success

    def onNodeSelectionChanged(self, node: QObject, selected: bool) -> None:
        """Event handler invoked when selection state changes on any of the nodes"""
        assertRef(node)
        assertTrue(isinstance(node, Node))
        if selected:
            Log.debug("Updating selected node")
            self.__selected_node = node
        elif node is self.__selected_node and not selected:
            Log.debug("Clearing selected node")
            self.__selected_node = None
        self.selected_node_changed.emit(self.__selected_node)

    def clearAll(self) -> None:
        """
        Removes all content from the scene.

        """
        self.deleteAllNodes()
        self.removeAllNodeConnections()
        self.__name_generator.reset()
