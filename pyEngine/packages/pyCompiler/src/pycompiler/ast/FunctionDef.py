import ast
from typing import Any, Callable
from ..bytecode import Instruction, CodeObject
from ..compiler.Scope import Scope

def _compile_function_def(node: ast.FunctionDef, scope: Scope, callback: Callable) -> list[Instruction]:

    instructions: list[Instruction] = list()
    function_instructions: list[Instruction] = list()

    function_scope = scope.new(Scope.Type.FUNCTION, scope.verbose)

    function_instructions.extend(callback(node.args, function_scope))
    for statement in node.body: function_instructions.extend(callback(statement, function_scope))
    # TODO for decorator in node.decorator_list: instructions.extend(callback(decorator, function_scope))
    # TODO for type_param in node.type_params: instructions.extend(callback(type_param, function_scope))
    
    instructions.extend(scope.store_code(node.name, CodeObject.new(node.name, function_scope.locals, function_scope.globals, function_scope.instructions))) # returns []
    # states "func" should be stored in a constants table, the vm will read the function blueprint and store it in globals

    return instructions