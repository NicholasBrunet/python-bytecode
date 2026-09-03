import ast
from typing import Any
from ..bytecode import Instruction
from ..compiler.Scope import Scope

def _compile_constant(node: ast.Constant, scope: Scope) -> list[Instruction]:
    return scope.load_const(node.value)