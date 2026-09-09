"""
Python Virtual Runtime code module

contains opcodes bundled into instructions created into
a code object to be run by a virtual thread
"""

from __future__ import annotations

# -------------------------------------
# PYTHON BYTECODE INSTRUCTIONS
# -------------------------------------

# STORAGE OPERATIONS

LOAD_BUILTIN = 0

LOAD_STR = 1
LOAD_INT = 2
LOAD_FLOAT = 3
LOAD_CODE = 4

LOAD_NAME = 5
LOAD_FAST = 6

STORE_NAME = 7
STORE_FAST = 8

# COMPARISON OPERATIONS

COMPARE_OP = 9

# LIFECYCLE OPERATIONS

MAKE_FUNCTION = 10
RETURN_VALUE = 11

POP_JUMP_IF_FALSE = 12
CALL = 13

PUSH_NULL = 14
POP_TOP = 15
DUO_TOP = 16
SWAP = 17
HALT = 18

# BINARY OPERATIONS

BIN_ADD = 19
BIN_SUB = 20
BIN_MULT = 21
BIN_DIV = 22

# -------------------------------------

class CodeObject:
    """
    Blueprint describing the instructions for a virtual runtime to
    execute a custom bytecode format
    """
    
    __slots__ = ["name", "strs", "ints", "floats", "code", "instructions"]
    def __init__(
        self, 
        name: str, 
        strs: list[str],
        ints: list[int],
        floats: list[float],
        code: list[CodeObject], 
        instructions: bytearray
    ):
        self.name: str = name
        self.strs: list[str] = strs
        self.ints: list[int] = ints
        self.floats: list[float] = floats
        self.code: list[CodeObject] = code
        self.instructions: bytearray = instructions