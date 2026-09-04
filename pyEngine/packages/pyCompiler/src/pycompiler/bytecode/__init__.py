"""
Bytecode module
"""

from .Instruction import Instruction
from .Opcode import Opcode
from .CodeObject import CodeObject

__all__ = [
    "Instruction",
    "Opcode",
    "CodeObject",
]