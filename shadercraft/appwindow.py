from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow, QVBoxLayout
from PySide6.QtCore import Qt

from .asserts import assertTrue
from .node import Node
from .shadernodes import OutputShaderNode, ShaderNodeBase, FloatShaderNode, MulShaderNode
from .windowbase import Ui_MainWindow
from .nodegraphscene import NodeGraphScene
from .nodegraphview import NodeGraphView
from .nodepalette import NodePaletteWidget


class AppWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Create and setup node graph viewport
        self.graph_view: NodeGraphView = NodeGraphView()
        self.graph_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graph_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graph_view.setDragMode(QGraphicsView.NoDrag)
        self.ui.NodeGraphFrame.layout().addWidget(self.graph_view)

        self._initPalette()

        self.graph_scene: NodeGraphScene = NodeGraphScene()
        self.graph_view.setScene(self.graph_scene)
        self.graph_view.update()
        asp = self.graph_view.rect().width() / self.graph_view.rect().height()
        self.graph_view.setSceneRect(0, 0, 2000, 2000/asp)
 
        self.ui.actionGenerate_Shader_Code.triggered.connect(self.onGenerateShaderCode)

    def _initPalette(self) -> None:
        """
        Create and initialise node palatte panel
        """
        self.palette_widget: NodePaletteWidget = NodePaletteWidget(self)
        self.ui.PaletteFrame.setLayout(QVBoxLayout())
        self.ui.PaletteFrame.layout().addWidget(self.palette_widget)

        self.palette_widget.addPaletteItems([
            FloatShaderNode,
            MulShaderNode,
            OutputShaderNode
        ])

        self.palette_widget.refresh()

    def onGenerateShaderCode(self) -> None:
        """
        Event handler invoked when genrate shader code menu item is clicked.
        For the time being we simply dump the shader code to the console.
        """
        print("Generating shader code")
        output_nodes: OutputShaderNode = self.graph_scene.getAllNodeOfClass(OutputShaderNode)
        if output_nodes is None:
            print("Attempting to generate shader code with no output node in the scene, aborting.")
            return
        assertTrue(len(output_nodes) == 1)
        output_node: Node = output_nodes[0]
        shader_nodes: list[Node] = output_node.getDownstreamNodes()

        for node in shader_nodes:
            assertTrue(isinstance(node, ShaderNodeBase))
            shader_summary: str = node.generateShaderCodeSummary()
            shader_src: str = node.generateShaderCode()
            print(shader_summary)
            print(shader_src)
            print("\r\n")

        print("Done")
