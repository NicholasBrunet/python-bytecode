import ast
from typing import Any
from ..bytecode import Instruction
from .Scope import Scope

def _compile_argument(node: ast.arg, scope: Scope) -> list[Instruction]:
    return []