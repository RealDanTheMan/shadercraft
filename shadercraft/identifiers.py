from __future__ import annotations
from uuid import UUID, uuid5, uuid4

# This seed is used for deterministic UUID generation
UUID_SEED: UUID = UUID("8b6badb9-97dd-436b-b5bd-eb1dc7032344")

def genUUID(name: str = None):
    """
    Geneterates deterministick uuid based on given name or unqiue one.

    """
    if name is not None:
        return uuid5(UUID_SEED, name)
    return uuid4()
