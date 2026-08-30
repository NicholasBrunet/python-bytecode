from __future__ import annotations

from enum import Enum, auto


class Opcode(Enum):
    """
    Represents an instruction understood by the game virtual machine.
    """
    def _generate_next_value_(name, start, count, last_values):
        return f"{count:09b}"

    # STORAGE OPERATIONS
    LOAD_CONST = auto()

    LOAD_GLOBAL = auto()
    STORE_GLOBAL = auto()

    LOAD_LOCAL = auto()
    STORE_LOCAL = auto()

    # CALL OPERATIONS
    # CALL_API = BinaryId.next()

    # LIFECYCLE OPERATIONS
    POP_TOP = auto()
    DUO_TOP = auto()
    HALT = auto()

    # BINARY OPERATIONS
    BIN_ADD = auto()
    BIN_SUB = auto()
    BIN_MULT = auto()
    BIN_DIV = auto()

    def __str__(self) -> str:
        return self.name

    @classmethod
    def of_binary(cls, binary_str: str) -> Opcode:
        return cls(binary_str)