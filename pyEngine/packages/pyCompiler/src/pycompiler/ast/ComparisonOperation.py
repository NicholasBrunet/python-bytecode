import ast

from ..compiler import Scope
from ..bytecode.Instruction import Instruction

comparators = {
    ast.Lt: 0,
    ast.LtE: 1,
    ast.Eq: 2,
    ast.NotEq: 3,
    ast.Gt: 4,
    ast.GtE: 5
}

def _compile_comparison_operation(node: ast.cmpop, scope: Scope) -> list[Instruction]:
    return scope.compare_op(comparators[node.__class__])