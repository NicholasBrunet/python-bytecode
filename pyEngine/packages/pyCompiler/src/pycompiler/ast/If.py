import ast
from typing import Any, Callable
from ..bytecode import Instruction
from ..compiler.Scope import Scope

def _compile_if(node: ast.If, scope: Scope, callback: Callable) -> list[Instruction]:

    instructions: list[Instruction] = list()
    body_instructions: list[Instruction] = list()

    if_statement_scope = scope.new(Scope.Type.IF_STATEMENT, scope.globals, scope.constants, scope.verbose)
    for statement in node.body: 
        body_instructions.extend(callback(statement, if_statement_scope))
    
    instructions.extend(callback(node.test, scope))
    scope.pop_jump_if_false(len(body_instructions))
    instructions.extend(if_statement_scope.collapse("N/A"))
    for statement in node.orelse: instructions.extend(callback(statement, scope))

    return instructions