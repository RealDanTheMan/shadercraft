from __future__ import annotations
import re
import logging as Log

from .asserts import assertType, assertRef, assertTrue

class NameDeduplicator():
    """
    Class responsible for identifying duplcate names and enforcing name uniqueness.

    """

    def __init__(self):
        """
        Default constructor.

        """
        self.__pool_cache: dict[str, list[int]] = {}
        self.__name_cache: dict[str, int] = {}
        self.__unames: set[str] = []

    def reset(self) -> None:
        """
        Clears deduplicator caches freeing all allocated names.

        """
        self.__pool_cache.clear()
        self.__name_cache.clear()
        self.__unames.clear()

    def registerName(self, name: str) -> str:
        """
        Deduplicates given name ensuring its uniquness.

        Parameters:
            name (str) : Input name to deduplicate.

        Returns:
            Uniquified name

        """
        assertType(name, str)
        assertTrue(name != "")

        base_name, num = self.__deconstructName(name)
        if base_name in self.__name_cache:
            self.__name_cache[base_name] += 1
        else:
            self.__name_cache[base_name] = 0

        if base_name in self.__pool_cache and len(self.__pool_cache[base_name]) > 0:
            num = self.__pool_cache[base_name].pop(0)
        else:
            num = self.__name_cache[base_name]

        uname: str = f"{base_name}{num}"
        assertTrue(uname not in self.__unames, f"Deduplicator failed with name -> {uname}")
        self.__unames.append(uname)

        return uname

    def deregisterName(self, name: str) -> None:
        """
        Removes given name from deduplication cache essentially allocating its future availability.

        """
        assertType(name, str)
        assertTrue(name != "")

        base_name, num = self.__deconstructName(name)
        if base_name in self.__name_cache:
            self.__unames.remove(name)
            self.__name_cache[base_name] -= 1
            if base_name not in self.__pool_cache:
                self.__pool_cache[base_name] = []
            self.__pool_cache[base_name].append(num)
            self.__pool_cache[base_name].sort()

        return

    def containsName(self, name: str) -> bool:
        """
        Returns True if given name already exists.

        """
        return name in self.__unames

    @staticmethod
    def __deconstructName(name: str) -> tuple[str, int]:
        """
        Deconstruct the name into base name string and numerical suffix.

        Example :
        input='SomeName3', Ouput: ('SomeName', 3)
        input='SomeName', Output: ('SomeName', 0)

        Parameters:
            name (str) : Input name to deconstruct

        Returns:
            Tuple[str, int] : Base name string, numerical suffix

        """
        regex_match: re.Match = re.match(r"^(.+?)(\d+)$", name)
        if regex_match:
            #Log.debug(f"Deduplicator name '{name}' deconstructed: Group 1 -> '{regex_match.group(1)}'")
            #Log.debug(f"Deduplicator name '{name}' deconstructed: Group 2 -> '{regex_match.group(2)}'")
            base_name: str = regex_match.group(1)
            suffix: int = int(regex_match.group(2))

            return (base_name, suffix)
        return (name, 0)
