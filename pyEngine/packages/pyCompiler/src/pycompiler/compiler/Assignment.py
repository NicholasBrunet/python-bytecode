import ast
from typing import Any
from ..bytecode.Instruction import Instruction

def _compile_assignment(node: ast.Assign, flags: dict[str, Any]) -> list[Instruction]:

    instructions: list[Instruction] = list()

    instructions.extend(flags["callback"](node.value))
    for i, target in enumerate(reversed(node.targets)):
        if i < len(node.targets) - 1: instructions.append(Instruction.duplicate_top())
        instructions.extend(flags["callback"](target))

    return instructions