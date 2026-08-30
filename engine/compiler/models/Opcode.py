from __future__ import annotations

from enum import Enum


class Opcode(Enum):
    """
    Represents an instruction understood by the game virtual machine.
    """

    # STORAGE OPERATIONS
    LOAD_CONST = "load_const"

    LOAD_GLOBAL = "load_global"
    STORE_GLOBAL = "store_global"

    LOAD_LOCAL = "load_local"
    STORE_LOCAL = "store_local"

    # CALL OPERATIONS
    CALL_API = "call_api"

    # LIFECYCLE OPERATIONS
    POP_TOP = "pop_top"
    HALT = "halt"

    # BINARY OPERATIONS
    BIN_ADD = "bin_add"
    BIN_SUB = "bin_sub"
    BIN_MULT = "bin_mult"
    BIN_DIV = "bin_div"