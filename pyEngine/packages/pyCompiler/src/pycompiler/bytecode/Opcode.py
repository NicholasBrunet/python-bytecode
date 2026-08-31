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

    LOAD_NAME = auto()
    STORE_NAME = auto()
    """
    Store the value at the top of stack with a given identifier \n
    e.g. "x = 5"

    However the bytecode should emit identifiers as storage indexes
    """
    
    # COMPARISON OPERATIONS
    COMPARE_OP = auto()  # Operand will represent the type of check (e.g., "==", "<")


    # LIFECYCLE OPERATIONS
    MAKE_FUNCTION = auto()
    CALL_FUNCTION = auto()
    RETURN_VALUE = auto()

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