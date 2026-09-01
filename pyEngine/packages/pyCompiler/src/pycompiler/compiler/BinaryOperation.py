import ast
from typing import Any, Callable
from ..bytecode.Instruction import Instruction
from .CompilerError import CompilerError
from .Scope import Scope

def _compile_binary_operation(node: ast.Compare, scope: Scope, callback: Callable) -> list[Instruction]:

    instructions: list[Instruction] = list()

    instructions.extend(callback(node.left, scope))
    instructions.extend(callback(node.right, scope))

    match node.op:
        case ast.Add(): instructions.extend(scope.binary_add)
        case ast.Sub(): instructions.append(scope.binary_subtract)
        case ast.Mult(): instructions.append(scope.binary_multiply)
        case ast.Div(): instructions.append(scope.binary_divide)
        case _: raise CompilerError(f"Unsupported math operator: {type(node.op).__name__}")

    return instructions