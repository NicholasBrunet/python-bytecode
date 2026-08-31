from __future__ import annotations

import ast
import json

from .bytecode.Instruction import Instruction
from .bytecode.Program import Program
from .compiler import CompilerError, _assign, _import, _name, _constant, _operator, _bin_op, _compare

class Compiler():

    def __init__(self):

        self._available_globals: dict[str, str] = {}# = {
        #     "game.World": "World",
        #     "game": "game"
        # }

        self._globals: dict[str, str] = {}
        self._locals: dict[str, str] = {}

        self._flags: dict [str, str] = {
            "scope": "module"
        }

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

        if isinstance(statement, ast.Import | ast.ImportFrom):
            return _import(statement, {
                "scope": self._flags["scope"],
                "load": self.__load,
                "store": self.__store
            })

        elif isinstance(statement, ast.Name):
            return _name(statement, {
                "scope": self._flags["scope"],
                "load": self.__load,
                "store": self.__store
            })

        elif isinstance(statement, ast.Constant):
            return _constant(statement, {
                "scope": "constant",
                "load": self.__load
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
                "compile": self._compile_statement
            })
        
        elif isinstance(statement, ast.BinOp):
            return _bin_op(statement, {
                "compile": self._compile_statement
            })
        
        elif isinstance(statement, ast.Compare):
            return _compare(statement, {
                "compile": self._compile_statement
            })

        else:
            raise CompilerError(f"Could not find compiler operation for: {statement.__class__}")



    def __store(self, key: object, scope: str) -> list[Instruction]:

        instructions: list[Instruction] = list()

        if scope == "module":

            if key not in self._globals: self._globals[key] = len(self._globals)
            storage_index = self._globals[key]

            instructions.append(Instruction.store_global(storage_index))

        else:

            if key not in self._locals: self._locals[key] = len(self._locals)
            storage_index = self._locals[key]

            instructions.append(Instruction.store_local(storage_index))

        return instructions


    def __load(self, key: object, scope: str) -> list[Instruction]:

        instructions: list[Instruction] = list()

        if scope == "module": 
            
            if key not in self._globals:
                if key in self._available_globals:
                    self._globals[key] = len(self._globals)
                else:
                    raise NameError(f"Name '{key}' is not defined.")
            
            storage_index = self._globals[key]

            instructions.append(Instruction.load_global(storage_index))
        elif scope == "constant": instructions.append(Instruction.load_const(key))
        else: 
            
            if key not in self._locals: raise NameError(f"Local name '{key}' is not defined.")

            instructions.append(Instruction.load_local(key))

        return instructions
