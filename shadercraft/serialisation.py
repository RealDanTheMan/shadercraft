from __future__ import annotations
from dataclasses import dataclass


@dataclass
class JSONChunk:
    """

    """
    data: dict
    version: int
    classname: str


class ISerialisableJSON():
    """

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
