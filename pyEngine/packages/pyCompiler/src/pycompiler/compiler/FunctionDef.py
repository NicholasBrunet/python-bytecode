import ast
from typing import Any
from ..bytecode.Instruction import Instruction

def _compile_function_def(node: ast.FunctionDef, flags: dict[str, Any]) -> list[Instruction]:

    instructions: list[Instruction] = list()

    return instructions