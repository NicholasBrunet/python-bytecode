import ast
from typing import Any, Callable
from ..bytecode import Instruction
from ..compiler.Scope import Scope

def _compile_return(node: ast.Return, scope: Scope, callback: Callable) -> list[Instruction]:

    instructions: list[Instruction] = list()

    instructions.extend(callback(node.value, scope))
    instructions.extend(scope.return_value)

    return instructions