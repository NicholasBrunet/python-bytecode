import ast
from typing import Any
from ..bytecode import Instruction
from ..compiler.Scope import Scope

def _compile_arg(node: ast.arg, scope: Scope) -> list[Instruction]:
    scope.storage_index(node.arg)
    return []