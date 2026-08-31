import ast
from typing import Any
from ..bytecode.Instruction import Instruction

def _compile_name(node: ast.Name, flags: dict[str, Any]) -> list[Instruction]:
    if isinstance(node.ctx, ast.Store): return flags["store"](node.id)
    elif isinstance(node.ctx, ast.Load): return flags["load"](node.id)
    else:
        raise ValueError(f"Found unknown ast.Name.ctx attribute: {node.ctx}")