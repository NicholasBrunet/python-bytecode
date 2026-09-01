import ast
from typing import Any
from ..bytecode.Instruction import Instruction

def _compile_comparison_operation(node: ast.cmpop, flags: dict[str, Any]) -> list[Instruction]:
    return [Instruction.compare_op(flags["comparators"][node.__class__])]