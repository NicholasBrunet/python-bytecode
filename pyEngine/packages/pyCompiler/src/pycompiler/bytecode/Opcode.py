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
    """
    Load constant of value onto the stack
    """

    LOAD_NAME = auto()
    STORE_NAME = auto()
    LOAD_FAST = auto()
    STORE_FAST = auto()
    
    # COMPARISON OPERATIONS
    COMPARE_OP = auto()


    # LIFECYCLE OPERATIONS
    MAKE_FUNCTION = auto()
    RETURN_VALUE = auto()

    POP_JUMP_IF_FALSE = auto()
    
    CALL = auto()

    PUSH_NULL = auto()
    POP_TOP = auto()
    DUO_TOP = auto()
    SWAP = auto()
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