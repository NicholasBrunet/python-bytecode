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

    def __init__(self, scope: Scope.Type, globals: dict[str, Any] = {}, parent_scope: Scope | None = None, verbose: bool = False):

        self._scope: Scope.Type = scope
        self._parent_scope: Scope | None = parent_scope

        # compiler will store identifiers in a dictionary, the vm will read from this dictionary and store in memory
        self._globals_index: dict[Any, int] = globals
        self._locals_index: dict[Any, int] = {}
        self._instructions: list[Instruction] = []

        self._verbose: bool = verbose

    def new(self, scope: Scope.Type, verbose: bool = False):
        return self.__class__(scope, self.globals, self, verbose)

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
    def storage(self) -> dict[Any, int]:
        if self.type == Scope.Type.MODULE: return self.globals
        elif self.type == Scope.Type.FUNCTION: return self.locals

    def storage_index(self, identifier: Any) -> int:
        if identifier not in self.storage.keys():
            self.storage[identifier] = len(self.storage)

        return self.storage[identifier]

    def dump(self) -> str:
        if self.peak_instructions:
            print(f"'{self.type}' '{self.peak_instructions}'")
    
    # STORAGE OPERATIONS

    def load_const(self, value: Any) -> list[Instruction]:

        instruction = self.push(Instruction.load_const(value))
    
        if self.verbose: self.dump()
        return [instruction]

    def load_name(self, identifier: Any) -> list[Instruction]:

        storage_index = self.storage_index(identifier)
        instruction = self.push(Instruction.load_name(storage_index))

        if self.verbose: self.dump()
        return [instruction]

    def store_name(self, identifier: Any) -> list[Instruction]:

        storage_index = self.storage_index(identifier)
        instruction = self.push(Instruction.store_name(storage_index))

        if self.verbose: self.dump()
        return [instruction]

    # COMPARISON OPERATIONS


    # FUNCTION OPERATIONS

    def make_function(self, name: str) -> list[Instruction]:

        if name not in self.constants.keys():
            self.constants[name] = len(self.constants)

        storage_index = self.constants[name]
        instruction = self.push(Instruction.make_function(storage_index))

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