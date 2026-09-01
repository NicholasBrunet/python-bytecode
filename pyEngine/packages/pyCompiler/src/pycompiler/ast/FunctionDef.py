import ast
from typing import Any, Callable
from ..bytecode import Instruction
from ..compiler.Scope import Scope

def _compile_function_def(node: ast.FunctionDef, scope: Scope, callback: Callable) -> list[Instruction]:

    instructions: list[Instruction] = list()

    function_scope = scope.new(Scope.Type.FUNCTION, scope.verbose)

    # only supports traditional arguments not type hinted e.g. func(a, b, c)
    for argument in node.args.args: instructions.extend(callback(argument, function_scope))
    for statement in node.body: instructions.extend(callback(statement, function_scope))

    return instructions