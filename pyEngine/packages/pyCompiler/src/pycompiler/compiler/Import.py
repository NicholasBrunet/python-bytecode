import ast
from typing import Any
from ..bytecode.Instruction import Instruction
from .Scope import Scope

def _compile_import(node: ast.Import | ast.ImportFrom, scope: Scope) -> list[Instruction]:

    try: 
        if node.level != 0: raise ValueError("Denied import: cannot perform relative imports, use module imports.")
    except AttributeError: ...

    if isinstance(node, ast.ImportFrom): module = node.module + "."
    else: module = ""

    instructions: list[Instruction] = list()

    for alias in node.names:
        
        import_key_identifier = module + alias.name
        identifier = alias.asname if alias.asname else alias.name
        instructions.extend(scope.load_name(import_key_identifier))
        instructions.extend(scope.store_name(identifier))

    return instructions