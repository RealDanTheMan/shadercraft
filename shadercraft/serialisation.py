from __future__ import annotations
from dataclasses import dataclass

from .asserts import assertType, assertRef, assertTrue

@dataclass
class JSONChunk:
    """
    Chunk represents a arbitrary section of JSON data in dictionary format.

    """
    data: dict
    version: int
    classname: str

    @classmethod
    def toJson(cls, chunk: JSONChunk) -> dict:
        """
        Serialises this chunk to JSON like dictionary

        """
        assertType(chunk, JSONChunk)
        assertType(chunk.classname, str)
        assertType(chunk.version, int)
        assertType(chunk.data, dict)

        data: dict = {
            "classname" : chunk.classname,
            "version"   : str(chunk.version),
            "data"      : chunk.data
        }

        return data

    @classmethod
    def fromJson(cls, data: dict) -> JSONChunk:
        """
        Dersialise JSON chunk from JSON like dictionary.

        """
        assertType(data, dict)
        assertTrue("classname" in data)
        assertTrue("version" in data)
        assertTrue("data" in data)

        return JSONChunk(
            data["data"],
            int(data["version"]),
            data["classname"]
        )


class ISerialisableJSON():
    """
    Interfave class responsible for serialising and deserialising JSON content.

    """

    @classmethod
    def serialiseJSON(cls, obj: object) -> JSONChunk:
        """
        Serialise the class that implements this interfave to JSON chunk.

        """
        raise NotImplementedError(
            "serialiseJSON() must be implemented in the subclass of ISerialisableJSON"
        )

    @classmethod
    def deserialiseJSON(cls, chunk: JSONChunk) -> object:
        """
        Deserialise class that implements this interface from JSON chunk.

        """
        raise NotImplementedError(
            "deserialiseJSON() must be implemented in the subclass of ISerialisableJSON"
        )
