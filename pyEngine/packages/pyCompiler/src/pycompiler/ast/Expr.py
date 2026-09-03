import ast
from typing import Any, Callable
from ..bytecode import Instruction
from ..compiler.Scope import Scope

def _compile_expr(node: ast.Expr, scope: Scope, callback: Callable) -> list[Instruction]:
    return list(callback(node.value, scope))