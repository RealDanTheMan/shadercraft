from __future__ import annotations
from uuid import UUID
import os
import logging as Log
import json


from .asserts import assertRef, assertType, assertTrue
from .node import Node
from .shadernodes import *
from .output_shadernodes import *

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

        Properties:
            node (Node) : Node to serialise.

        """
        assertRef(node)
        assertType(node, Node)

        data = {
            "version"       : str(self.version),
            "uuid"          : str(node.uuid),
            "type"          : str(type(node).__name__),
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

    def deserialiseNode(self, data: dict) -> Node:
        """
        Deserialises given JSON like data into graph node.

        Properties:
            data (dict) : JSON like dictionary object representing the node.
        
        """
        self.__buffer = {}
        self.__buffer.update(data)

        uuid        : UUID = UUID(self.__buffer["uuid"])
        node_class  : type = globals().get(self.__buffer["type"], None)
        name        : str = self.__buffer["name"]
        posx        : float = float(self.__buffer["posx"])
        posy        : float = float(self.__buffer["posy"])

        Log.debug(f"Parsed node -> {node_class} [name={name}, posx={posx}, posy={posy}, uuid={uuid}]")

        node: Node = node_class()
        node.uuid = uuid
        node.name = name
        node.posx = posx
        node.posy = posy

        for input_data in self.__buffer["inputs"]:
            pass

        return node

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

        Properties:
            nodes (list[Node]) : List of nodes that form the graph.
        """
        self.__node_serialiser: NodeSerialiser = NodeSerialiser()
        self.__buffer: str = None
        self.__nodes: list[Node] = []
        self.__nodes.extend(nodes)

    def getNodes(self) -> list[Node]:
        """
        Get list of active nodes.

        """
        return list(self.__nodes)

    def serialise(self) -> None:
        """
        Serialise all current nodes to active buffer.

        """
        Log.info(f"Serialising {len(self.__nodes)} nodes")

        data: dict = {
            "version" : str(self.version),
            "nodes" : []
        }

        for node in self.__nodes:
            assertRef(node)
            assertType(node, Node)

            Log.info(f"Serialising node -> {node}")
            self.__node_serialiser.clearBuffer()
            self.__node_serialiser.serialiseNode(node)
            data["nodes"].append(self.__node_serialiser.getBufferValue())

        self.__buffer = json.dumps(data, indent=2)

    def deserialise(self) -> None:
        """
        Deserialises all nodes from active buffer data.

        """
        assertRef(self.__buffer)
        Log.info("Deserialising node graph")

        self.__nodes.clear()
        data: dict = json.loads(self.__buffer)
        if data is not None:
            for node_data in data["nodes"]:
                node: Node = self.__node_serialiser.deserialiseNode(node_data)
                self.__nodes.append(node)

    def write(self, filepath: str) -> bool:
        """
        Write the contents of the active buffer to disk at given location using JSON format.

        Properties:
            filepath (str) : Filepath to write to.

        """
        assertRef(filepath)
        assertRef(self.__buffer)

        Log.info(f"Writing data file -> {filepath}")
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(self.__buffer)

        Log.info("Done")

    def read(self, filepath: str) -> None:
        """
        Read the contents of given JSON file and create shader graph nodes.

        Properties:
            filepath (str) : Filepath to read from.
        """
        assertType(filepath, str)
        assertTrue(os.path.exists(filepath))
        Log.info(f"Reading shader graph file -> {filepath}")

        self.__buffer = None
        with open(filepath, "r", encoding="utf-8") as file:
            self.__buffer = file.read()
