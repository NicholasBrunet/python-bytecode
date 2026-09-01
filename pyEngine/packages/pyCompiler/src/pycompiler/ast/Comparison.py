import ast
from typing import Any, Callable
from ..bytecode.Instruction import Instruction
from ..compiler.CompilerError import CompilerError
from ..compiler.Scope import Scope

def _compile_comparison(node: ast.Compare, scope: Scope, callback: Callable) -> list[Instruction]:

    if len(node.comparators) > 1: 
        raise CompilerError(
"""\n
pyCompiler does not support multiple comparison targets.
use parenthesis to allow multiple in-line comparisons.

E.g. 'x = 1 == 2 == 3', causes this error. use x = (1 == 2) == 3,
or any other valid arangement of 'a {op} b', where a or b can be
the result of another operation encapsulated by parenthesis.
""")

    instructions: list[Instruction] = list()

    instructions.extend(callback(node.left, scope))
    instructions.extend(callback(node.comparators[0], scope))
    instructions.extend(callback(node.ops[0], scope))

    return instructions