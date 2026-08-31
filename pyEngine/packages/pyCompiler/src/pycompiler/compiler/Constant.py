import ast
from typing import Any
from ..bytecode.Instruction import Instruction

def _compile_constant(node: ast.Constant, flags: dict[str, Any]) -> list[Instruction]:
    return flags["load"](node.value)