import ast
from typing import Any, Callable
from ..bytecode import Instruction
from ..compiler.Scope import Scope

def _compile_if_expression(node: ast.IfExp, scope: Scope, callback: Callable) -> list[Instruction]:

    instructions: list[Instruction] = list()


    return instructions