"""
Bytecode module
"""

from .Instruction import Instruction
from .Opcode import Opcode
from .Program import Program

__all__ = [
    "Instruction",
    "Opcode",
    "Program",
]