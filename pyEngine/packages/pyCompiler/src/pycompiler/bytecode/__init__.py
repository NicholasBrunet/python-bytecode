"""
Bytecode module
"""

from .Instruction import Instruction
from .Opcode import Opcode
from .Program import Program
from .CodeObject import CodeObject

__all__ = [
    "Instruction",
    "Opcode",
    "Program",
]