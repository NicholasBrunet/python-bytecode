"""
Primary module for pyCompiler

Contains:
    Compiler
    Program
    Instruction
    Opcode
"""

from ._Compiler import Compiler
from ._bytecode.Program import Program
from ._bytecode.Instruction import Instruction
from ._bytecode.Opcode import Opcode

__all__ = [
    "Compiler",
    "Program",
    "Instruction",
    "Opcode"
]