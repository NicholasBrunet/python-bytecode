import ast
from typing import Any, Callable
from ..bytecode import Instruction, CodeObject
from ..compiler.Scope import Scope

def _compile_function_def(node: ast.FunctionDef, scope: Scope, callback: Callable) -> list[Instruction]:

    instructions: list[Instruction] = list()
    function_instructions: list[Instruction] = list()

    function_scope = scope.new(Scope.Type.FUNCTION, {}, {}, scope.verbose)

    function_instructions.extend(callback(node.args, function_scope))
    for statement in node.body: function_instructions.extend(callback(statement, function_scope))
    # TODO for decorator in node.decorator_list: instructions.extend(callback(decorator, function_scope))
    # TODO for type_param in node.type_params: instructions.extend(callback(type_param, function_scope))

    # Collapse the function scope into a code object and store it in the parent scope's constants table
    function_scope.collapse(node.name)

    # Emit bytecode to load the function's code object from the constants table
    instructions.extend(scope.load_const(node.name))
    instructions.extend(scope.make_function)

    if scope.type == Scope.Type.FUNCTION: instructions.extend(scope.store_fast(node.name))
    else: instructions.extend(scope.store_name(node.name))

    
    return instructions