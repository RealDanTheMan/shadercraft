from __future__ import annotations
from dataclasses import dataclass
import logging as Log

from .asserts import assertType, assertTrue


#dataclass
class Vec2F:
    x: float = 0.0
    y: float = 0.0

    def __init__(self, xx: float, yy: float) -> None:
        assertType(xx, float)
        assertType(yy, float)
        self.x = xx
        self.y = yy

    def __str__(self) -> str:
        return f"{self.x},{self.y}"

    @staticmethod
    def parse(value: str) -> Vec2F:
        """
        Create new Vec2F value from given string literal.

        """
        assertType(value, str)
        values: list[str] = value.split(',')
        if len(values) == 2:
            try:
                x: float = float(values[0])
                y: float = float(values[1])
                return Vec2F(x, y)
            except:
                Log.error(f"Failed to parse Vec2F values from string: '{values}'")
                raise
        raise RuntimeError(f"Invalid Vec2F string value: '{values}")


class Vec3F:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __init__(self, xx: float, yy: float, zz: float):
        assertType(xx, float)
        assertType(yy, float)
        assertType(zz, float)
        self.x = xx
        self.y = yy
        self.z = zz

    def __str__(self) -> str:
        return f"{self.x},{self.y},{self.z}"

    @staticmethod
    def parse(value: str) -> Vec3F:
        """
        Create new Vec3F value from given string literal.

        """
        assertType(value, str)
        values: list[str] = value.split(',')
        if len(values) == 3:
            try:
                x: float = float(values[0])
                y: float = float(values[1])
                z: float = float(values[2])
                return Vec3F(x, y, z)
            except:
                Log.error(f"Failed to parse Vec3F values from string: '{values}'")
                raise
        raise RuntimeError(f"Invalid Vec3F string value: '{values}")

class Vec4F:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    w: float = 0.0

    def __init__(self, xx: float, yy: float, zz: float, ww: float):
        assertType(xx, float)
        assertType(yy, float)
        assertType(zz, float)
        assertType(ww, float)
        self.x = xx
        self.y = yy
        self.z = zz
        self.w = ww

    def __str__(self) -> str:
        return f"{self.x},{self.y},{self.z},{self.w}"

    @staticmethod
    def parse(value: str) -> Vec4F:
        """
        Create new Vec4F value from given string literal.

        """
        assertType(value, str)
        values: list[str] = value.split(',')
        if len(values) == 4:
            try:
                x: float = float(values[0])
                y: float = float(values[1])
                z: float = float(values[2])
                w: float = float(values[4])
                return Vec4F(x, y, z, w)
            except:
                Log.error(f"Failed to parse Vec4F values from string: '{values}'")
                raise
        raise RuntimeError(f"Invalid Vec4F string value: '{values}")
