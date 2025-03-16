import os
from typing import Type, Optional
import logging as Log
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QGraphicsView,
    QMainWindow,
    QVBoxLayout,
    QTextEdit,
    QFrame,
    QFileDialog
)

from .shadernodes import (
    ShaderNodeBase,
    FloatShaderNode,
    MulShaderNode,
    MakeVec3Node,
    LerpNode,
    LerpVecNode,
    VertexColorShaderNode,
    VertexNormalShaderNode,
    VertexPositionShaderNode,
    VectorToColor
)

from .output_shadernodes import (
    OutputShaderNodeBase,
    PhongOutputShaderNode
)

from .asserts import assertTrue, assertRef, assertType
from .node import Node, NodeClassDesc
from .windowbase import Ui_MainWindow
from .nodegraphscene import NodeGraphScene
from .nodegraphview import NodeGraphView
from .nodepalette import NodePaletteWidget
from .propertypanel import PropertyPanelWidget
from .viewportwidget import ViewportWidget
from .shadergen import ShaderGen
from .diskio import NodeGraphSerialiser


class AppWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.log_last_pos: int = 0
        self.log_refresh_rate: int = 100
        self.log_timer: QTimer = QTimer(self)
        self.preview_timer: QTimer = QTimer(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._initLogView()
        self._initGraph()
        self._initScene()
        self._initPalette()
        self._initPropertyPanel()
        self._initPreviewViewport()

        self.ui.actionSave_As.triggered.connect(self.onSaveAs)
        self.ui.actionOpen.triggered.connect(self.onOpenFile)
        self.ui.actionGenerate_Shader_Code.triggered.connect(self.onGenerateShaderCode)


    def _initPalette(self) -> None:
        """
        Create and initialise node palatte panel.
        """
        assertRef(self.ui.PaletteFrame)
        self.palette_widget: NodePaletteWidget = NodePaletteWidget(self)
        self.ui.PaletteFrame.setLayout(QVBoxLayout())
        self.ui.PaletteFrame.layout().addWidget(self.palette_widget)

        self.palette_widget.addPaletteItems([
            VertexPositionShaderNode,
            VertexColorShaderNode,
            VertexNormalShaderNode,
            FloatShaderNode,
            MulShaderNode,
            MakeVec3Node,
            LerpNode,
            LerpVecNode,
            VectorToColor,
            PhongOutputShaderNode
        ])

        self.palette_widget.createNodeRequested.connect(self.onPaletteNodeRequested)
        self.palette_widget.refresh()

    def _initGraph(self) -> None:
        """
        Create and setup node graph view.
        """
        self.graph_view: NodeGraphView = NodeGraphView()
        self.graph_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graph_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graph_view.setDragMode(QGraphicsView.NoDrag)

        assertRef(self.ui.NodeGraphFrame)
        self.ui.NodeGraphFrame.layout().addWidget(self.graph_view)

    def _initScene(self) -> None:
        """
        Create and setup node graph scene.
        """
        assertRef(self.graph_view)
        self.graph_scene: NodeGraphScene = NodeGraphScene()
        self.graph_scene.selected_node_changed.connect(self.onGraphNodeSelectionChanged)
        self.graph_scene.preview_redraw_requested.connect(self.onPreviewRedrawRequested)
        self.graph_view.setScene(self.graph_scene)
        self.graph_view.update()
        self.graph_scene.addDefaultNodes()
        asp = self.graph_view.rect().width() / self.graph_view.rect().height()
        self.graph_view.setSceneRect(0, 0, 10000, 10000/asp)

    def _initLogView(self) -> None:
        self.log_view: QTextEdit = QTextEdit(parent=self)
        self.log_view.setObjectName("LogView")
        self.log_view.setReadOnly(True)
        self.ui.OutputViewFrame.setLayout(QVBoxLayout())
        self.ui.OutputViewFrame.layout().addWidget(self.log_view)
        self.updateLogView()

        self.log_timer.timeout.connect(self.updateLogView)
        self.log_timer.startTimer(self.log_refresh_rate)

    def _initPropertyPanel(self) -> None:
        self.property_panel: PropertyPanelWidget = PropertyPanelWidget(self)
        self.property_panel.preview_redraw_requested.connect(self.onPreviewRedrawRequested)
        self.ui.PropertiesPanelFrame.setLayout(QVBoxLayout())
        self.ui.PropertiesPanelFrame.layout().addWidget(self.property_panel)

    def _initPreviewViewport(self) -> None:
        Log.info("Initialising preview viewport")
        frame: QFrame = self.ui.PreviewViewportFrame
        assertRef(frame)

        self.preview_viewport: ViewportWidget = ViewportWidget(parent=frame)
        self.preview_viewport.setMinimumHeight(128)
        self.preview_viewport.setMinimumWidth(128)
        frame.setLayout(QVBoxLayout())
        frame.layout().addWidget(self.preview_viewport)

        # Set viewport to redraw at 60Hz
        self.preview_timer.timeout.connect(self.preview_viewport.requestRedraw)
        self.preview_timer.start(16)

    def updateLogView(self) -> None:
        """
        Update the log view contents.
        Contents of the log view are sourced form active app log file.
        """
        assertRef(self.log_view)
        log_file: str = self.getLogFile()
        if not os.path.exists(log_file):
            Log.error(f"Failed to located active log file -> {log_file}")
            return

        try:
            with open(log_file, "r") as file:
                file.seek(self.log_last_pos)
                lines: list[str] = file.readlines()
                for line in lines:
                    self.log_view.append(line)
                self.log_last_pos = file.tell()
        except Exception as e:
            Log.error(f"Failed to parse logging file -> {log_file}")
            print(e)
        self.log_timer.start(self.log_refresh_rate)


    def onPaletteNodeRequested(self, node_desc: NodeClassDesc) -> None:
        """Event handler invoked when node palette panel requests node creation"""
        Log.debug(f"Adding new '{node_desc.label}' node to the graph on palette request")
        assertRef(node_desc)
        assertTrue(node_desc.node_type)

        node: Node = node_desc.node_type()
        self.graph_scene.addNode(node)

    def onPreviewRedrawRequested(self, rebuild_shader: bool = True) -> None:
        """
        Event handler invoked when various app panels action request redraw of preview viewport.
        This can be slow if it triggers shader recompilation.
        """
        assertType(rebuild_shader, bool)
        assertRef(self.preview_viewport)
        Log.debug("Preview redraw requested")

        if rebuild_shader:
            self.onGenerateShaderCode()
        self.preview_viewport.requestRedraw()

    def onGenerateShaderCode(self) -> None:
        """
        Event handler invoked when genrate shader code menu item is clicked.
        Collects all the graph shader nodes and generates shader source code.
        """
        Log.info("Generating shader code")
        output_nodes: OutputShaderNodeBase = self.graph_scene.getAllNodeOfClass(OutputShaderNodeBase)
        if output_nodes is None:
            Log.warning("Attempting to generate shader code with no output node in the scene, aborting.")
            return
        assertTrue(len(output_nodes) == 1)
        output_node: Node = output_nodes[0]
        shader_nodes: list[Node] = output_node.getDownstreamNodes()

        gen: ShaderGen = ShaderGen()
        gen.generateSource(shader_nodes)
        gen.writeSource(".")

        # Load generate shade into preview viewport
        assertRef(self.preview_viewport)
        stat: bool = self.preview_viewport.requestShader(gen.vertex_shader, gen.pixel_shader)
        if not stat:
            Log.error("Failed to compile generated shader code")

        Log.info("Done")

    def onGraphNodeSelectionChanged(self, node: Node) -> None:
        """
        Event handler invoked when selected node changes inside graph scene.
        We use this trigger to update property panel with selected node values.
        """
        assertRef(self.property_panel)
        self.property_panel.setActiveNode(node)
        self.property_panel.fetchNodeValues()

    def onSaveAs(self) -> None:
        """
        Event handler invoked when the user clicks on save as option from the file menu.
        Allows the user to select location on disk where the shader graph is serialised to.
        """
        Log.debug("Attempting to save node graph to disk")
        assertRef(self.graph_scene)

        destination: tuple[str, str] = QFileDialog.getSaveFileName(self, "Save As", filter="*.scg")
        if destination is not None and len(destination) > 0:
            filepath: str = destination[0]
            if filepath is None or len(filepath) == 0:
                return

            if not os.path.exists(filepath):
                nodes: list[Node] = self.graph_scene.getAllNodes()
                serialiser: NodeGraphSerialiser = NodeGraphSerialiser(nodes)
                serialiser.serialise()
                serialiser.write(destination[0])
            else:
                # TODO: Handle overwriting files and readonly flags.
                Log.error(f"Node graph file already exists, aborting -> {filepath}")

        return

    def onOpenFile(self) -> None:
        """
        Event handler invoked when the user clicks on open file option from the file menu.
        Allow the user to select shader graphs file to load.
        
        """
        Log.debug("Attempting to load node graph from disk.")

        self.graph_scene.clear()
        source:tuple[str, str] = QFileDialog.getOpenFileName(self, "Open File", filter="*.scg")
        if source is not None and len(source) > 0:
            filepath: str = source[0]
            if filepath is None or len(filepath) == 0:
                return

            serialiser: NodeGraphSerialiser = NodeGraphSerialiser([])
            serialiser.read(filepath)
            serialiser.deserialise()

            nodes: list[Node] = serialiser.getNodes()
            for node in nodes:
                self.graph_scene.addNode(node)
            Log.info(f"Loaded {len(nodes)} nodes")


    @staticmethod
    def getLogFile() -> Optional[str]:
        """Get first active log file"""
        for handler in Log.getLogger().handlers:
            if isinstance(handler, Log.FileHandler):
                return handler.baseFilename
        return None
