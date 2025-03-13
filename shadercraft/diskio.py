from __future__ import annotations
import logging as Log
import json

from .asserts import assertRef, assertType
from .node import Node
from .shadernodes import ShaderNodeIO 

class NodeSerialiser():
    """
    Class responsible for serialising any node class to json like buffer object.

    """
    version: int = 1

    def __init__(self):
        """
        Default constructor.

        """
        self.__buffer: dict = {}

    def serialiseNode(self, node: Node) -> None:
        """
        Serialises given node to json like buffer object.

        """
        assertRef(node)
        assertType(node, Node)

        data = {
            "version"       : str(self.version),
            "uuid"          : str(node.uuid),
            "type"          : str(type(node)),
            "name"          : node.name,
            "posx"          : str(node.posx),
            "posy"          : str(node.posy),
        }

        # Serialise node connections.
        for connection in node.getAllConnections():
            conn_data: dict = {
                "src_node"      : str(connection.source.uuid),
                "src_output"    : str(connection.source_uuid),
                "input"         : str(connection.target_uuid)
            }

            if "connections" not in data:
                data["connections"] = []
            data["connections"].append(conn_data)

        # Serialise node input static values.
        for node_in in node.getNodeInputs():
            if isinstance(node_in, ShaderNodeIO):
                input_data: dict = {
                    "uuid"  : str(node_in.uuid),
                    "name"  : node_in.name,
                    "value" : str(node_in.static_value)
                }

                if "inputs" not in data:
                    data["inputs"] = []
                data["inputs"].append(input_data)


        self.__buffer.update(data)

    def getBufferValue(self) -> str:
        """
        Get copy of the inner json like buffer object.

        """
        val: dict = {}
        val.update(self.__buffer)
        return val

    def clearBuffer(self) -> None:
        """
        Clear internal buffer object.

        """
        self.__buffer = {}


class NodeGraphSerialiser():
    """
    Responsible for serialising entire shader graph contents to JSON file on disk.

    """
    version: int = 1

    def __init__(self, nodes: list[Node]):
        """
        Default constructor.
        """
        self.__node_serialiser: NodeSerialiser = NodeSerialiser()
        self.__buffer: str = None
        self.__nodes: list[Node] = []
        self.__nodes.extend(nodes)

    def serialise(self) -> None:
        """
        Serialise all current nodes to active buffer.

        """
        Log.info(f"Serialising {len(self.__nodes)} nodes")

        data: dict = {
            "version" : str(self.version),
            "nodes" : []
        }

        serialiser: NodeSerialiser = NodeSerialiser()
        for node in self.__nodes:
            assertRef(node)
            assertType(node, Node)

            Log.info(f"Serialising node -> {node}")
            serialiser.clearBuffer()
            serialiser.serialiseNode(node)
            data["nodes"].append(serialiser.getBufferValue())

        self.__buffer = json.dumps(data, indent=2)

    def write(self, filepath: str) -> bool:
        """
        Write the contents of the active buffer to disk at given location using JSON format.

        """
        assertRef(filepath)
        assertRef(self.__buffer)

        Log.info(f"Writing data file -> {filepath}")
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(self.__buffer)

        Log.info("Done")
