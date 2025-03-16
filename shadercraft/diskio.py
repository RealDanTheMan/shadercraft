from __future__ import annotations
from uuid import UUID
import os
import logging as Log
import json


from .asserts import assertRef, assertType, assertTrue
from .node import Node
from .shadernodes import *
from .output_shadernodes import *
from .serialisation import JSONChunk


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
            chunk: JSONChunk = node.__class__.serialiseJSON(node)
            node_data: dict = {}

            node_data["classname"] = chunk.classname
            node_data["version"] = str(chunk.version)
            node_data["data"] = chunk.data

            data["nodes"].append(node_data)

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
                chunk: JSONChunk = JSONChunk(
                    node_data["data"],
                    int(node_data["version"]),
                    node_data["classname"]
                )

                node_cls: type = globals().get(chunk.classname, None)
                node: Node = node_cls.deserialiseJSON(chunk)
                assertRef(node)
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
