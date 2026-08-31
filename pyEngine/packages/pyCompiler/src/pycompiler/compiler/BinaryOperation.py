import ast
from typing import Any
from ..bytecode.Instruction import Instruction
from .CompilerError import CompilerError

def _compile_binary_operation(node: ast.Compare, flags: dict[str, Any]) -> list[Instruction]:

    instructions: list[Instruction] = list()

    instructions.extend(flags["compile"](node.left))
    instructions.extend(flags["compile"](node.right))

    match node.op:
        case ast.Add(): instructions.append(Instruction.binary_add())
        case ast.Sub(): instructions.append(Instruction.binary_subtract())
        case ast.Mult(): instructions.append(Instruction.binary_multiply())
        case ast.Div(): instructions.append(Instruction.binary_divide())
        case _:
            raise CompilerError(f"Unsupported math operator: {type(node.op).__name__}")

    return instructions