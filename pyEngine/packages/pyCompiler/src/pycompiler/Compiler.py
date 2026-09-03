from __future__ import annotations

import ast
import json
from typing import Any

from .bytecode import Instruction, Program, CodeObject
from .compiler import CompilerError, Scope
from .ast import (
    _assign, _import, _name, _constant, _operator, 
    _bin_op, _compare, _func_def, _arg, _return,
    _expr, _arguments, _call, _module
)

class Compiler():

    def __init__(self):

        self._globals: dict[str, Any] = {
            "print": 0
        }
        self._scope: Scope | None

    def compile(self, source: str, verbose: bool = False):
        
        try:
            module = ast.parse(source, mode='exec')
        except SyntaxError as e:
            error_line = e.text.rstrip('\n') if e.text else ""
            
            start = e.offset - 1 if e.offset else 0
            end = getattr(e, 'end_offset', e.offset) - 1 if getattr(e, 'end_offset', None) else start + 1
            
            caret_count = max(1, end - start)
            padding = " " * start
            carets = "^" * caret_count

            raise CompilerError(
f"""\n
File "<unknown>", line {e.lineno}
    {error_line}
    {padding}{carets}
SyntaxError: {e.msg}
""")


        if verbose: print(ast.dump(module, indent=4))
        self._scope = Scope(Scope.Type.MODULE, self._globals, None, verbose)
        instructions: list[Instruction] = self._compile_statement(module, self._scope)

        return CodeObject.new("module", self._scope.locals, self._scope.globals, instructions)



    def _compile_statement(self, statement: ast.stmt, scope: Scope) -> list[Instruction]:

        if isinstance(statement, ast.Module):
            return _module(statement, scope, self._compile_statement)
        
        elif isinstance(statement, ast.Constant):
            return _constant(statement, scope)
    
        elif isinstance(statement, ast.Import | ast.ImportFrom):
            return _import(statement, scope)

        elif isinstance(statement, ast.Name):
            return _name(statement, scope)
        
        elif isinstance(statement, ast.cmpop):
            return _operator(statement)
        
        elif isinstance(statement, ast.Assign):
            return _assign(statement, scope, self._compile_statement)
        
        elif isinstance(statement, ast.BinOp):
            return _bin_op(statement, scope, self._compile_statement)
        
        elif isinstance(statement, ast.Compare):
            return _compare(statement, scope, self._compile_statement)
        
        elif isinstance(statement, ast.FunctionDef):
            return _func_def(statement, scope, self._compile_statement)
        
        elif isinstance(statement, ast.arguments):
            return _arguments(statement, scope, self._compile_statement)

        elif isinstance(statement, ast.arg):
            return _arg(statement, scope)
        
        elif isinstance(statement, ast.Return):
            return _return(statement, scope, self._compile_statement)

        elif isinstance(statement, ast.Expr):
            return _expr(statement, scope, self._compile_statement)
        
        elif isinstance(statement, ast.Call):
            return _call(statement, scope, self._compile_statement)
        
        else:
            raise CompilerError(f"Could not find compiler operation for: {statement.__class__}")