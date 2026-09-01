import ast
from typing import Any
from ..bytecode.Instruction import Instruction
from .Scope import Scope

def _compile_name(node: ast.Name, scope: Scope) -> list[Instruction]:
    if isinstance(node.ctx, ast.Store): return scope.store_name(node.id)
    elif isinstance(node.ctx, ast.Load): return scope.load_name(node.id)
    else:
        raise ValueError(f"Found unknown ast.Name.ctx attribute: {node.ctx}")