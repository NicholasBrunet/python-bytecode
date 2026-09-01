from __future__ import annotations

from typing import Any, Literal
from ..bytecode import Instruction, CodeObject, Opcode

from enum import Enum, auto

# WARNING: look into sub-classing with new() method
class Scope:
    class Type(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return f"{count:04b}"
        
        MODULE = auto()
        FUNCTION = auto()

    def __init__(self, scope: Scope.Type, globals: dict[Any, int] = {}, parent_scope: Scope | None = None, verbose: bool = False):

        self._scope: Scope.Type = scope
        self._parent_scope: Scope | None = parent_scope

        self._globals: dict[Any, int] = globals
        self._locals: dict[Any, int] = {}
        self._constants: dict[Any, int] = {}

        self._verbose: bool = verbose

        self._stack: list[Any] = [] # live stack
        self._instructions: list[Instruction] = []

    def new(self, scope: Scope.Type, verbose: bool = False):
        return self.__class__(scope, self.globals, self, verbose)

    @property
    def type(self) -> Scope.Type:
        return self._scope
    
    @property
    def verbose(self) -> bool:
        return self._verbose
    
    @property
    def stack(self) -> list[Any]:
        return self._stack
    
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
        return self._globals
    
    @property
    def locals(self) -> dict[Any, int]:
        return self._locals

    @property
    def constants(self) -> dict[Any, int]:
        return self._constants
    
    @property
    def storage(self) -> dict[Any, int]:
        if self.type == Scope.Type.MODULE: return self.globals
        elif self.type == Scope.Type.FUNCTION: return self.locals

    def pop_stack(self) -> Any:
        return self._stack.pop()
    
    @property
    def peak_stack(self) -> Any:
        return self.stack[-1]

    def push_stack(self, value: Any):
        self._stack.append(value)

    def dump(self) -> str:
        print(f"'{self.peak_instructions}': {self.stack}")
    
    # STORAGE OPERATIONS

    def load_const(self, value: Any) -> list[Instruction]:

        self.push_stack(value)
        instruction = self.push(Instruction.load_const(value))
    
        if self.verbose: self.dump()
        return [instruction]

    def load_name(self, identifier: Any) -> list[Instruction]:
        if self.verbose: self.dump()
        self.push_stack(identifier)
        if identifier not in self.storage.keys():
            self.storage[identifier] = len(self.storage)

        storage_index = self.storage[identifier]
        instruction = self.push(Instruction.load_name(storage_index))

        if self.verbose: self.dump()
        return [instruction]

    def store_name(self, identifier: Any) -> list[Instruction]:
        self.pop_stack()
        if identifier not in self.storage.keys():
            self.storage[identifier] = len(self.storage)

        storage_index = self.storage[identifier]
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

        self.pop_stack()
        instruction = self.push(Instruction.return_value())

        if self.verbose: self.dump()
        return [instruction]

    # LIFECYCLE OPERATIONS

    @property
    def duplicate_top(self) -> list[Instruction]:

        self.push_stack(self.peak_stack)
        instruction = self.push(Instruction.duplicate_top())

        if self.verbose: self.dump()
        return [instruction]
    
    # BINARY OPERATIONS

    @property
    def binary_add(self) -> Instruction:
        right = self.pop_stack()
        left = self.pop_stack()
        self.push_stack(left + right)

        instruction = self.push(Instruction.binary_add())

        if self.verbose: self.dump()
        return [instruction]
    
    @property
    def binary_subtract(self) -> Instruction:
        right = self.pop_stack()
        left = self.pop_stack()
        self.push_stack(left - right)

        instruction = self.push(Instruction.binary_subtract())

        if self.verbose: self.dump()
        return [instruction]
    
    @property
    def binary_multiply(self) -> Instruction:
        right = self.pop_stack()
        left = self.pop_stack()
        self.push_stack(left * right)
        
        instruction = self.push(Instruction.binary_multiply())

        if self.verbose: self.dump()
        return [instruction]

    @property
    def binary_divide(self) -> Instruction:
        right = self.pop_stack()
        left = self.pop_stack()
        self.push_stack(left / right)
        
        instruction = self.push(Instruction.binary_divide())

        if self.verbose: self.dump()
        return [instruction]