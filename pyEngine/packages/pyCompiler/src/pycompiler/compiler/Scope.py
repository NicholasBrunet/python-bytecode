from __future__ import annotations

from typing import Any
from ..bytecode import Instruction

from enum import Enum, auto

# WARNING: look into sub-classing with new() method
class Scope:
    class Type(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return f"{count:04b}"
        
        MODULE = auto()
        FUNCTION = auto()

    def __init__(self, scope: Scope.Type, globals: dict[Any, int] = {}, parent_scope: Scope | None = None):

        self._scope: Scope.Type = scope
        self._parent_scope: Scope | None = parent_scope

        self._globals: dict[Any, int] = globals
        self._locals: dict[Any, int] = {}
        self._constants: dict[Any, int] = {}
        # maps identifier to storage key, mostly used for ease of reading

    def new(self, scope: Scope.Type):
        return self.__class__(scope, self.globals, self)

    @property
    def type(self) -> Scope.Type:
        return self._scope
    
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
    def storage(self) -> dict[Any, int]:
        if self.scope == Scope.Type.MODULE: return self.globals
        elif self.scope == Scope.Type.FUNCTION: return self.locals

    def load_constant(self, value: Any) -> list[Instruction]:
        return [Instruction.load_const(value)]

    def load_name(self, identifier: Any) -> list[Instruction]:
        if identifier not in self.storage.keys():
            self.storage[identifier] = len(self.storage)

        storage_index = self.storage[identifier]

        return [Instruction.load_name(storage_index)]

    def store_name(self, identifier: Any) -> list[Instruction]:
        if identifier not in self.storage.keys():
            self.storage[identifier] = len(self.storage)

        storage_index = self.storage[identifier]

        return [Instruction.store_name(storage_index)]