import ast
from typing import Any
from ..bytecode.Instruction import Instruction

def _compile_name(node: ast.Name, flags: dict[str, Any]) -> list[Instruction]:
    if isinstance(node.ctx, ast.Store): return flags["store"](node.id, flags["scope"])
    elif isinstance(node.ctx, ast.Load): return flags["load"](node.id, flags["scope"])
    else:
        raise ValueError(f"Found unknown ast.Name.ctx attribute: {node.ctx}")