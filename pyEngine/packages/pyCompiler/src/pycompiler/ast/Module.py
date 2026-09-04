import ast
from typing import Any, Callable
from ..bytecode import Instruction
from ..compiler.Scope import Scope

def _compile_module(node: ast.Module, scope: Scope, callback: Callable) -> list[Instruction]:

    instructions: list[Instruction] = list()

    for statement in node.body: instructions.extend(callback(statement, scope))
    instructions.extend(scope.return_value)

    return instructions