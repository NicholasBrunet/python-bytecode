import ast
from typing import Any
from ..bytecode.Instruction import Instruction

comparators = {
    ast.Lt: 0,
    ast.LtE: 1,
    ast.Eq: 2,
    ast.NotEq: 3,
    ast.Gt: 4,
    ast.GtE: 5
}

def _compile_comparison_operation(node: ast.cmpop) -> list[Instruction]:
    return [Instruction.compare_op(comparators[node.__class__])]