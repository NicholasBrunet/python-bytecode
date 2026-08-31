from __future__ import annotations

import ast
import json

from .bytecode import (
    Instruction,
    Program
)
from .compiler import (
    CompilerError, Scope,
    _assign, _import, _name, _constant, _operator, 
    _bin_op, _compare, _func_def
)

class Compiler():

    def __init__(self):

        self._globals: dict[str, str] = {}
        """
        Globals passed into module scope, this allows
        compiler to block certain imports of unauthorized
        globals.
        """

        self._scope: Scope = Scope(Scope.Type.MODULE, self._globals)

    def compile(self, source: str, verbose: bool = False):
        
        try:
            tree = ast.parse(source, mode='exec')
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


        if verbose: print(ast.dump(tree, indent=4))

        instructions: list[Instruction] = list()

        for statement in tree.body:
            if verbose: print(f"Visiting node: {ast.dump(statement)}")

            if statement != None:
                instructions.extend(self._compile_statement(statement))

        if verbose: print("Globals: " + json.dumps(self._globals, indent=4))
        if verbose: print("Locals: " + json.dumps(self._locals, indent=4))
        if verbose: print(f"Instructions: {[instruction.__str__() for instruction in instructions]}")

        return Program.of(instructions)



    def _compile_statement(self, statement: ast.stmt) -> list[Instruction]:

        if isinstance(statement, ast.Constant):
            return _constant(statement, {
                "load": self._scope.load_constant
            })
    
        elif isinstance(statement, ast.Import | ast.ImportFrom):
            return _import(statement, {
                "load": self._scope.load_name,
                "store": self._scope.store_name,
            })

        elif isinstance(statement, ast.Name):
            return _name(statement, {
                "load": self._scope.load_name,
                "store": self._scope.store_name,
            })
        
        elif isinstance(statement, ast.cmpop):
            return _operator(statement, {
                "comparators": {
                    ast.Lt: 0,
                    ast.LtE: 1,
                    ast.Eq: 2,
                    ast.NotEq: 3,
                    ast.Gt: 4,
                    ast.GtE: 5
                }
            })
        
        elif isinstance(statement, ast.Assign):
            return _assign(statement, {
                "callback": self._compile_statement
            })
        
        elif isinstance(statement, ast.BinOp):
            return _bin_op(statement, {
                "callback": self._compile_statement
            })
        
        elif isinstance(statement, ast.Compare):
            return _compare(statement, {
                "callback": self._compile_statement
            })
        
        elif isinstance(statement, ast.FunctionDef):
            _function_scope = self._scope.new(Scope.Type.FUNCTION)
            return _func_def(statement, {
                "callback": self._compile_statement,
                "load": _function_scope.load_name,
                "store": _function_scope.store_name
            })

        else:
            raise CompilerError(f"Could not find compiler operation for: {statement.__class__}")