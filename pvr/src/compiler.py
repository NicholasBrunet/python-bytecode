from __future__ import annotations
import ast
import argparse

from .code import (
    CodeObject,
    LOAD_BUILTIN, LOAD_STR, LOAD_INT, LOAD_FLOAT, LOAD_CODE, LOAD_FAST, LOAD_NAME,
    STORE_NAME, STORE_FAST, 
    MAKE_FUNCTION, RETURN_VALUE, POP_JUMP_IF_FALSE, CALL,
    PUSH_NULL, POP_TOP, DUO_TOP, SWAP, HALT,
    BIN_ADD, BIN_SUB, BIN_MULT, BIN_DIV, COMPARE_OP,
)

from .constants import (
    MAX_SCOPE_GLOBALS,
    MAX_SCOPE_LOCALS,
    MAX_SCOPE_PRIMITIVES,
    MAX_SCOPE_INSTRUCTIONS,
    MAX_SCOPE_CODE_OBJECTS,
    MAX_SCOPE_STACK,
    SCOPE_MODULE,
    SCOPE_FUNCTION,

    BUILTINS_MAP
)

_is = isinstance
_len = len
_str = str
_type = type

class CompilerError(Exception): ...

class Scope:

    __slots__ = ["type", "parent_scope", "globals_map", "globals_list", 
                 "locals_map", "locals_list", "instructions", "instruction_count", 
                 "stack_count", "str_map", "str_list", "int_map", "int_list",
                 "float_map", "float_list", "code_map", "code_list"]
    def __init__(self, type: int = SCOPE_MODULE, parent_scope: Scope | None = None):

        self.type: int = type
        self.parent_scope: Scope | None = parent_scope

        self.instructions: bytearray = bytearray(MAX_SCOPE_INSTRUCTIONS * 2)

        self.instruction_count: int = 0
        self.stack_count: int = 0 

        self.code_map: dict[str, int] = dict()
        self.code_list: list[CodeObject] = []

        self.locals_map: dict[str, int] = dict()
        self.locals_list: list[str] = []

        if parent_scope != None:
                
            self.globals_map: dict[str, int] = parent_scope.globals_map
            self.globals_list: list[str] = parent_scope.globals_list

            self.str_map: dict[str, int] = parent_scope.str_map
            self.str_list: list[str] = parent_scope.str_list

            self.int_map: dict[int, int] = parent_scope.int_map
            self.int_list: list[int] = parent_scope.int_list

            self.float_map: dict[float, int] = parent_scope.float_map
            self.float_list: list[float] = parent_scope.float_list

        else:

            self.globals_map: dict[str, int] = dict()
            self.globals_list: list[str] = []

            self.str_map: dict[str, int] = dict()
            self.str_list: list[str] = []

            self.int_map: dict[int, int] = dict()
            self.int_list: list[int] = []

            self.float_map: dict[float, int] = dict()
            self.float_list: list[float] = []

    def new(self, type: int) -> Scope:
        return Scope(type, self)

    def collapse_instructions(self) -> bytearray:
        self.parent_scope = None
        return self.instructions[0 : self.instruction_count]

    def collapse_code(self, name: str) -> CodeObject:
        self.parent_scope = None
        return CodeObject(name, 
                          self.str_list, 
                          self.int_list, 
                          self.float_list, 
                          self.code_list, 
                          self.instructions[0 : self.instruction_count])

    def add_instruction(self, opcode: int, operand: int):

        idx = self.instruction_count
        if idx + 2 > MAX_SCOPE_INSTRUCTIONS * 2:
            raise CompilerError("Max instructions for scope reached")

        self.instructions[idx] = opcode
        self.instructions[idx + 1] = operand
        self.instruction_count += 2

    def add_instructions(self, instructions: bytearray, count: int):

        idx = self.instruction_count
        if idx + count > MAX_SCOPE_INSTRUCTIONS * 2:
            raise CompilerError("Max instructions for scope reached")
        self.instructions[idx : idx + count] = instructions[0 : count]
        self.instruction_count += count

    def store(self, value: str, alias: str = "") -> tuple[int, int]:

        # print(f"Visiting scope.store(): {value}, {storage_id}")

        storage_id = self.type

        if storage_id == SCOPE_MODULE:
            if value in self.globals_map:
                pointer = self.globals_map[value]
            else:
                pointer = _len(self.globals_list)
                self.globals_map[value] = pointer
                self.globals_list.append(value)

            if _len(self.globals_list) >= MAX_SCOPE_GLOBALS:
                raise CompilerError("Max globals for scope reached.")

            return (STORE_NAME, pointer)

        elif storage_id == SCOPE_FUNCTION:
            if value in self.locals_map:
                pointer = self.locals_map[value]
            else:
                pointer = _len(self.locals_list)
                self.locals_map[value] = pointer
                self.locals_list.append(value)

            if _len(self.locals_list) >= MAX_SCOPE_LOCALS:
                raise CompilerError("Max locals for scope reached.")
            
            return (STORE_FAST, pointer)

        else:
            raise CompilerError("Unknown storage ID: '" + _str(storage_id) + "'")

    def load_code(self, code_object: CodeObject) -> tuple[int, int]:

        name = code_object.name

        if name in self.code_map:
            pointer = self.code_map[name]
            self.code_list[pointer] = code_object
        else:
            pointer = _len(self.code_list)
            self.code_map[name] = pointer
            self.code_list.append(code_object)

        if _len(self.code_list) >= MAX_SCOPE_CODE_OBJECTS:
            raise CompilerError("Max code objects for scope reached.")

        return (LOAD_CODE, pointer)
        
    def load(self, value: str) -> tuple[int, int]:

        # print(f"Visiting scope.load(): {value}, {storage_id}")

        storage_id = self.type

        if storage_id == SCOPE_MODULE:
            if value in self.globals_map:
                return (LOAD_NAME, self.globals_map[value])
            elif value in BUILTINS_MAP:
                return (LOAD_BUILTIN, BUILTINS_MAP[value])
            else:
                raise CompilerError("NameError: global name '" + value + "' is not defined.")

        elif storage_id == SCOPE_FUNCTION:
            if value in self.locals_map:
                return (LOAD_FAST, self.locals_map[value])
            elif value in self.globals_map:
                return (LOAD_NAME, self.globals_map[value])
            else:
                raise CompilerError("NameError: global/local name '" + value + "' is not defined.")
        
        else:
            raise CompilerError("Unknown storage ID: '" + _str(storage_id) + "'")

    def load_primitive(self, value: object) -> tuple[int, int]:

        if _is(value, _str):

            if value in self.str_map:
                pointer = self.str_map[value]
            else:
                pointer = _len(self.str_list)
                self.str_map[value] = pointer
                self.str_list.append(value)

            if _len(self.str_list) >= MAX_SCOPE_PRIMITIVES:
                raise CompilerError("Max string constants reached.")
            
            return (LOAD_STR, pointer)

        elif _is(value, int):

            if value in self.int_map:
                pointer = self.int_map[value]
            else:
                pointer = _len(self.int_list)
                self.int_map[value] = pointer
                self.int_list.append(value)

            if _len(self.int_list) >= MAX_SCOPE_PRIMITIVES:
                raise CompilerError("Max integer constants reached.")
            
            return (LOAD_INT, pointer)

        elif _is(value, float):

            if value in self.float_map:
                pointer = self.float_map[value]
            else:
                pointer = _len(self.float_list)
                self.float_map[value] = pointer
                self.float_list.append(value)

            if _len(self.float_list) >= MAX_SCOPE_PRIMITIVES:
                raise CompilerError("Max float constants reached.")
            
            return (LOAD_FLOAT, pointer)

        else:
            raise CompilerError("Unsupported primitive literal type: '" + _str(_type(value)) + "'")

    


class Compiler:

    @classmethod
    def compile_module(cls, module: ast.Module, name: str) -> CodeObject:

        module_scope = Scope()

        for statement in module.body:
            cls.compile_statement(statement, module_scope)

        module_scope.add_instruction(RETURN_VALUE, 0)

        return module_scope.collapse_code(name)

    @classmethod
    def compile_statement(cls, statement: ast.stmt, scope: Scope):

        # print(f"Visiting: {statement.__class__} | Scope: {scope.type} | Globals: {scope.globals_list}")

        if _is(statement, ast.Constant):
            scope.add_instruction(*scope.load_primitive(statement.value))

        elif _is(statement, ast.Import):

            for alias in statement.names:
                cls.compile_statement(alias, scope)

        elif _is(statement, ast.ImportFrom):

            module = statement.module

            if not module:
                raise CompilerError("Relative imports are not supported.")

            for alias in statement.names:
                alias.name = module + "." + alias.name
                cls.compile_statement(alias, scope)

        elif _is(statement, ast.alias):

            asname = statement.asname
            name = statement.name

            alias = name if asname == None else asname

            scope.add_instruction(*scope.load(name))
            scope.add_instruction(*scope.store(alias))

        elif _is(statement, ast.Name):

            if _is(statement.ctx, ast.Store):
                scope.add_instruction(*scope.store(statement.id))
            elif _is(statement.ctx, ast.Load):
                print(statement.id)
                scope.add_instruction(*scope.load(statement.id))
            else:
                raise CompilerError("Unknown statement: '" + _str(_type(statement.ctx)) + "'")
            
        elif _is(statement, ast.Assign):

            # TODO handle chained assignements
            cls.compile_statement(statement.value, scope)
            cls.compile_statement(statement.targets[0], scope)
            # for i, target in enumerate(reversed(node.targets)):
            #     if i < len(node.targets) - 1: instructions.extend(scope.duplicate_top())
            #     instructions.extend(callback(target, scope))
        
        elif _is(statement, ast.BinOp):

            cls.compile_statement(statement.left, scope)
            cls.compile_statement(statement.right, scope)

            if _is(statement.op, ast.Add):
                scope.add_instruction(BIN_ADD, 0)
            elif _is(statement.op, ast.Sub):
                scope.add_instruction(BIN_SUB, 0)
            elif _is(statement.op, ast.Mult):
                scope.add_instruction(BIN_MULT, 0)
            elif _is(statement.op, ast.Div):
                scope.add_instruction(BIN_DIV, 0)
            else:
                raise CompilerError("Unsupported binary operation: '" + _str(_type(statement)) + "'")
    
        elif _is(statement, ast.Compare):

            # TODO handle chained comparisons
            if _len(statement.comparators) > 1: 
                raise CompilerError("Compiler currently does not support chained comparisons.")

            cls.compile_statement(statement.left, scope)
            cls.compile_statement(statement.comparators[0], scope)
            cls.compile_statement(statement.ops[0], scope)

        elif _is(statement, ast.cmpop):

            if _is(statement, ast.Lt):
                scope.add_instruction(COMPARE_OP, 0)
            elif _is(statement, ast.LtE):
                scope.add_instruction(COMPARE_OP, 1)
            elif _is(statement, ast.Eq):
                scope.add_instruction(COMPARE_OP, 2)
            elif _is(statement, ast.NotEq):
                scope.add_instruction(COMPARE_OP, 3)
            elif _is(statement, ast.Gt):
                scope.add_instruction(COMPARE_OP, 4)
            elif _is(statement, ast.GtE):
                scope.add_instruction(COMPARE_OP, 5)
            else:
                raise CompilerError("Unsupported comparison operator: '" + _str(_type(statement)) + "'")
        
        elif _is(statement, ast.FunctionDef):

            function_scope = scope.new(SCOPE_FUNCTION)

            cls.compile_statement(statement.args, function_scope)
            for body_statement in statement.body:
                cls.compile_statement(body_statement, function_scope)
            
            # TODO for decorator in node.decorator_list: instructions.extend(callback(decorator, function_scope))
            # TODO for type_param in node.type_params: instructions.extend(callback(type_param, function_scope))
        
            code_object = function_scope.collapse_code(statement.name)
            scope.add_instruction(*scope.load_code(code_object))
            scope.add_instruction(MAKE_FUNCTION, 0)
            scope.add_instruction(*scope.store(statement.name))
        
        elif _is(statement, ast.arguments):

            # TODO for pos_arg in node.posonlyargs: instructions.extend(callback(pos_arg, scope))
            for arg in statement.args: 
                cls.compile_statement(arg, scope)
            # TODO for var_arg in node.vararg: instructions.extend(callback(var_arg, scope))
            # TODO for kwonly_arg in node.kwonlyargs: instructions.extend(callback(kwonly_arg, scope))
            # TODO for kw_default in node.kw_defaults: instructions.extend(callback(kw_default, scope))
            # TODO for kwarg in node.kwarg: instructions.extend(callback(kwarg, scope))
            # TODO for default in node.defaults: instructions.extend(callback(default, scope))

        elif _is(statement, ast.arg):

            scope.store(statement.arg)
        
        elif _is(statement, ast.Return):

            cls.compile_statement(statement.value, scope)
            scope.add_instruction(RETURN_VALUE, 0)

        elif _is(statement, ast.Expr):

            cls.compile_statement(statement.value)
        
        elif _is(statement, ast.Call):

            scope.add_instruction(PUSH_NULL, 0)
            cls.compile_statement(statement.func, scope)

            arg_counter = 0
            for arg in statement.args: 
                cls.compile_statement(arg, scope)
                arg_counter += 1

            # TODO for keyword in node.keywords: instructions.extend(callback(keyword.value, scope))
            scope.add_instruction(CALL, arg_counter)

        elif _is(statement, ast.If):
            
            cls.compile_statement(statement.test, scope)

            temp_scope = scope.new(scope.type)
            for body_statement in statement.body:
                cls.compile_statement(body_statement, temp_scope)

            scope.add_instruction(POP_JUMP_IF_FALSE, temp_scope.instruction_count)
            scope.add_instructions(temp_scope.collapse_instructions(), temp_scope.instruction_count)

            for orelse_statement in statement.orelse:
                cls.compile_statement(orelse_statement, scope)

        else:
            raise CompilerError("Unknown statement: '" + _str(_type(statement)) + "'")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Compile python 3.12 source code into bytecode")

    parser.add_argument("source", type=str, help="python source code")
    args = parser.parse_args()

    try:
        ast_module = ast.parse(args.source, mode='exec')
    except Exception as e:
        raise CompilerError(e)

    code_object = Compiler.compile_module(ast_module, "module")
    print(list(code_object.instructions))
    
