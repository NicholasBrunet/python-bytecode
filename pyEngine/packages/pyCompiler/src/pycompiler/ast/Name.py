import ast
from typing import Any
from ..bytecode.Instruction import Instruction
from ..compiler.Scope import Scope

def _compile_name(node: ast.Name, scope: Scope) -> list[Instruction]:
    if isinstance(node.ctx, ast.Store): return scope.scope_store(node.id)
    elif isinstance(node.ctx, ast.Load): return scope.scope_load(node.id)
    else:
        raise ValueError(f"Found unknown ast.Name.ctx attribute: {node.ctx}")