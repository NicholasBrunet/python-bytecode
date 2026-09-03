import ast
from typing import Any, Callable
from ..bytecode import Instruction
from ..compiler.Scope import Scope

def _compile_arguments(node: ast.arguments, scope: Scope, callback: Callable) -> list[Instruction]:

    instructions: list[Instruction] = []

    # TODO for pos_arg in node.posonlyargs: instructions.extend(callback(pos_arg, scope))
    for arg in node.args: instructions.extend(callback(arg, scope))
    # TODO for var_arg in node.vararg: instructions.extend(callback(var_arg, scope))
    # TODO for kwonly_arg in node.kwonlyargs: instructions.extend(callback(kwonly_arg, scope))
    # TODO for kw_default in node.kw_defaults: instructions.extend(callback(kw_default, scope))
    # TODO for kwarg in node.kwarg: instructions.extend(callback(kwarg, scope))
    # TODO for default in node.defaults: instructions.extend(callback(default, scope))

    return instructions