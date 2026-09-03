import ast
from typing import Any, Callable
from ..bytecode.Instruction import Instruction
from ..compiler.Scope import Scope

def _compile_assignment(node: ast.Assign, scope: Scope, callback: Callable) -> list[Instruction]:

    instructions: list[Instruction] = list()

    instructions.extend(callback(node.value, scope))
    for i, target in enumerate(reversed(node.targets)):
        if i < len(node.targets) - 1: instructions.extend(scope.duplicate_top())
        instructions.extend(callback(target, scope))

    return instructions