import ast
from typing import Any, Callable
from ..bytecode import Instruction
from ..compiler.Scope import Scope

def _compile_call(node: ast.Call, scope: Scope, callback: Callable) -> list[Instruction]:

    instructions: list[Instruction] = list()

    instructions.extend(scope.push_null)
    instructions.extend(callback(node.func, scope))
    for arg in node.args: instructions.extend(callback(arg, scope))
    # TODO for keyword in node.keywords: instructions.extend(callback(keyword.value, scope))
    instructions.extend(scope.call(len(node.args)))

    return instructions