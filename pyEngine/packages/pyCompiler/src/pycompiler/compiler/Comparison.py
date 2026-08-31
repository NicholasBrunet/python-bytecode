import ast
from typing import Any
from ..bytecode.Instruction import Instruction
from .CompilerError import CompilerError

def _compile_comparison(node: ast.BinOp, flags: dict[str, Any]) -> list[Instruction]:

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

    instructions.extend(flags["compile"](node.left))
    instructions.extend(flags["compile"](node.comparators[0]))
    instructions.extend(flags["compile"](node.ops[0]))

    return instructions