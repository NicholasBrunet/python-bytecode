from __future__ import annotations

from typing import Any, Literal

from ..bytecode import Instruction, CodeObject

from enum import Enum, auto

# WARNING: look into sub-classing with new() method
class Scope:
    class Type(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return f"{count:04b}"
        
        MODULE = auto()
        FUNCTION = auto()
        IF_STATEMENT = auto()

    def __init__(self, scope: Scope.Type, globals: dict[str, Any] = {}, constants: dict[Any, Any] = {}, parent_scope: Scope | None = None, verbose: bool = False):

        self._scope: Scope.Type = scope
        self._parent_scope: Scope | None = parent_scope

        # compiler will store identifiers in a dictionary, the vm will read from this dictionary and store in memory
        self._globals_index: dict[Any, int] = globals
        self._locals_index: dict[Any, int] = {}
        self._constants: dict[Any, Any] = constants

        self._instructions: list[Instruction] = []

        self._verbose: bool = verbose

    def new(self, scope: Scope.Type, globals: dict[str, Any] = {}, constants: dict[Any, Any] = {}, verbose: bool = False):
        return self.__class__(scope, globals, constants, self, verbose)

    # SCOPE PROPERTIES / FUNCTIONS

    @property
    def type(self) -> Scope.Type:
        return self._scope
    
    @property
    def verbose(self) -> bool:
        return self._verbose
    
    @property
    def instructions(self) -> list[Instruction]:
        return self._instructions

    @property
    def peak_instructions(self) -> Instruction | None:
        if len(self._instructions) == 0: return None
        return self._instructions[-1]
    
    def push(self, instruction: Instruction) -> Instruction:
        self._instructions.append(instruction)
        return instruction
    
    @property
    def parent_scope(self) -> Scope:
        return self._parent_scope
    
    @property
    def globals(self) -> dict[Any, int]:
        return self._globals_index
    
    @property
    def locals(self) -> dict[Any, int]:
        return self._locals_index

    @property
    def constants(self) -> dict[Any, int]:
        return self._constants

    def scope_load(self, identifier: Any) -> list[Instruction]:

        parent_type = self.parent_scope.type if self.parent_scope != None else None
        if self.type == Scope.Type.FUNCTION:
            if identifier in self.locals:
                return self.load_fast(identifier)
        return self.load_name(identifier)

    def scope_store(self, identifier: Any) -> list[Instruction]:

        parent_type = self.parent_scope.type if self.parent_scope != None else None
        if self.type == Scope.Type.FUNCTION:
            if identifier in self.locals: 
                return self.store_fast(identifier)
        return self.store_name(identifier)

    def storage_index(self, identifier: Any, storage: dict[Any, int]) -> int:
        if identifier not in storage.keys():
            storage[identifier] = len(storage)

        return storage[identifier]

    def collapse(self, name: str) -> CodeObject | list[Instruction]:
        obj: CodeObject | list[Instruction]
        if self.type != Scope.Type.IF_STATEMENT:
            code_object = CodeObject.new(name, self.locals, self.globals, self.constants, self.instructions)
            if self.parent_scope != None:
                self.parent_scope.constants[name] = code_object

            obj = code_object
        else:
            if self.parent_scope != None:
                self.parent_scope.instructions.extend(self.instructions)
            obj = list(self.instructions)

        self._scope = None
        self._parent_scope = None
        self._globals_index = None
        self._constants = None

        return obj
    
    def dump(self) -> str:
        if self.peak_instructions:
            print(f"'{self.type}' '{self.peak_instructions}'")

    # STORAGE OPERATIONS

    def load_const(self, identifier: Any) -> list[Instruction]:

        storage_index = self.storage_index(identifier, self.constants)
        instruction = self.push(Instruction.load_const(storage_index))
    
        if self.verbose: self.dump()
        return [instruction]

    def load_name(self, identifier: Any) -> list[Instruction]:

        storage_index = self.storage_index(identifier, self.globals)
        instruction = self.push(Instruction.load_name(storage_index))

        if self.verbose: self.dump()
        return [instruction]

    def store_name(self, identifier: Any) -> list[Instruction]:

        storage_index = self.storage_index(identifier, self.globals)
        instruction = self.push(Instruction.store_name(storage_index))

        if self.verbose: self.dump()
        return [instruction]

    def load_fast(self, identifier: Any) -> list[Instruction]:

        storage_index = self.storage_index(identifier, self.locals)
        instruction = self.push(Instruction.load_fast(storage_index))

        if self.verbose: self.dump()
        return [instruction]

    def store_fast(self, identifier: Any) -> list[Instruction]:

        storage_index = self.storage_index(identifier, self.locals)
        instruction = self.push(Instruction.store_fast(storage_index))

        if self.verbose: self.dump()
        return [instruction]

    # COMPARISON OPERATIONS

    def compare_op(self, op_identifier: int) -> list[Instruction]:

        instruction = self.push(Instruction.compare_op(op_identifier))

        if self.verbose: self.dump()
        return [instruction]


    # FUNCTION OPERATIONS

    @property
    def make_function(self) -> list[Instruction]:

        instruction = self.push(Instruction.make_function())

        if self.verbose: self.dump()
        return [instruction]

    @property
    def return_value(self) -> list[Instruction]:

        instruction = self.push(Instruction.return_value())

        if self.verbose: self.dump()
        return [instruction]

    # LIFECYCLE OPERATIONS

    @property
    def push_null(self) -> list[Instruction]:

        instruction = self.push(Instruction.push_null())

        if self.verbose: self.dump()
        return [instruction]

    def pop_jump_if_false(self, jump_amount: int) -> list[Instruction]:

        instruction = self.push(Instruction.pop_jump_if_false(jump_amount))

        if self.verbose: self.dump()
        return [instruction]


    @property
    def duplicate_top(self) -> list[Instruction]:

        instruction = self.push(Instruction.duplicate_top())

        if self.verbose: self.dump()
        return [instruction]
    
    def call(self, argument_count: int) -> list[Instruction]:

        instruction = self.push(Instruction.call(argument_count))

        if self.verbose: self.dump()
        return [instruction]
    
    # BINARY OPERATIONS

    @property
    def binary_add(self) -> Instruction:

        instruction = self.push(Instruction.binary_add())

        if self.verbose: self.dump()
        return [instruction]
    
    @property
    def binary_subtract(self) -> Instruction:

        instruction = self.push(Instruction.binary_subtract())

        if self.verbose: self.dump()
        return [instruction]
    
    @property
    def binary_multiply(self) -> Instruction:

        instruction = self.push(Instruction.binary_multiply())

        if self.verbose: self.dump()
        return [instruction]

    @property
    def binary_divide(self) -> Instruction:

        instruction = self.push(Instruction.binary_divide())

        if self.verbose: self.dump()
        return [instruction]