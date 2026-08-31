from __future__ import annotations

import ast
import json

from .bytecode.Instruction import Instruction
from .bytecode.Program import Program

class CompilerError(Exception):
    """
    Raised when player source code cannot be compiled into game bytecode.
    """

class Compiler():

    def __init__(self):

        self._available_globals: dict[str, str] = {
            "game.World": "World",
            "game": "game"
        }

        self._globals: dict[str, str] = {}
        self._locals: dict[str, str] = {}

        self._flags: dict [str, str] = {
            "scope": "module"
        }

        self._comparison_map = {
            ast.Lt: 0,
            ast.LtE: 1,
            ast.Eq: 2,
            ast.NotEq: 3,
            ast.Gt: 4,
            ast.GtE: 5
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

            # Print the exact format you want
            print(f'File "<unknown>", line {e.lineno}')
            print(f'    {error_line}')
            print(f'    {padding}{carets}')
            print(f'SyntaxError: {e.msg}')
            return

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
            return self._compile_import(statement)

        elif isinstance(statement, ast.Assign):
            return self._compile_assignment(statement)

        elif isinstance(statement, ast.Name):
            return self._compile_name(statement)

        elif isinstance(statement, ast.Constant):
            return self._compile_constant(statement)
        
        elif isinstance(statement, ast.BinOp):
            return self._compile_binary_operation(statement)
        
        elif isinstance(statement, ast.Compare):
            return self._compile_comparison(statement)
        
        elif isinstance(statement, ast.cmpop):
            return self._compile_comparison_operation(statement)

        else:
            raise ValueError(f"Could not find compiler operation for: {statement.__class__}")



    def _compile_import(self, node: ast.Import | ast.ImportFrom) -> list[Instruction]:

        try: 
            if node.level != 0: raise ValueError("Denied import: cannot perform relative imports, use module imports.")
        except AttributeError: ...
    
        if isinstance(node, ast.ImportFrom): module = node.module + "."
        else: module = ""

        instructions: list[Instruction] = list()

        for alias in node.names:
            key = module + alias.name
            if key in self._available_globals: # RULE: can only import a global if in available globals

                name = alias.asname if alias.asname else alias.name
                instructions.extend(self.__load(key, self._flags["scope"]))
                instructions.extend(self.__store(name, self._flags["scope"]))

            else:
                raise ValueError(f"Denied import: {key}, not in available globals.")

        return instructions
    

    def _compile_assignment(self, node: ast.Assign) -> list[Instruction]:

        instructions: list[Instruction] = list()

        instructions.extend(self._compile_statement(node.value))
        for i, target in enumerate(reversed(node.targets)):
            if i < len(node.targets) - 1: instructions.append(Instruction.duplicate_top())
            instructions.extend(self._compile_statement(target))

        return instructions


    def _compile_name(self, node: ast.Name) -> list[Instruction]:
        if isinstance(node.ctx, ast.Store): return self.__store(node.id, self._flags["scope"])
        elif isinstance(node.ctx, ast.Load): return self.__load(node.id, self._flags["scope"])
        else:
            raise ValueError(f"Found unknown ast.Name.ctx attribute: {node.ctx}")


    def _compile_constant(self, node: ast.Constant) -> list[Instruction]:
        return self.__load(node.value, "constant")

    
    def _compile_binary_operation(self, node: ast.Compare) -> list[Instruction]:

        instructions: list[Instruction] = list()

        instructions.extend(self._compile_statement(node.left))
        instructions.extend(self._compile_statement(node.right))
        instructions.extend(self.__operation(node.op))

        return instructions

    
    def _compile_comparison(self, node: ast.BinOp) -> list[Instruction]:

        instructions: list[Instruction] = list()

        # needs to be fixed!
        for right in reversed(node.comparators): instructions.extend(self._compile_statement(right))
        instructions.extend(self._compile_statement(node.left))
        for operator in reversed(node.ops): instructions.extend(self._compile_statement(operator))

        return instructions

    def _compile_comparison_operation(self, node: ast.cmpop) -> list[Instruction]:
        return [Instruction.compare_op(self._comparison_map[node.__class__])]







    def __operation(self, operation: ast.operator) -> list[Instruction]:
        match operation:
            case ast.Add(): return [Instruction.binary_add()]
            case ast.Sub(): return [Instruction.binary_subtract()]
            case ast.Mult(): return [Instruction.binary_multiply()]
            case ast.Div(): return [Instruction.binary_divide()]
            case _:
                raise NotImplementedError(f"Unsupported math operator: {type(operation).__name__}")


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
