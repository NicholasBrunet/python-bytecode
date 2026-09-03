from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import Any

from .Instruction import Instruction

@dataclass(frozen=True)
class CodeObject:
    """
    An immutable blueprint representing compiled code (a script, function, or method).
    Trapped inside constants tables until instantiated by the VM.
    """
    _name: str = ""
    _locals: dict[Any, int] = field(default_factory=dict)
    _globals: dict[Any, int] = field(default_factory=dict)
    _instructions: list[Instruction] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self._name

    @property
    def locals(self) -> dict[Any, int]:
        return self._locals

    @property
    def globals(self) -> dict[Any, int]:
        return self._globals
    
    @property
    def instructions(self) -> list[Instruction]:
        return self._instructions

    @classmethod
    def new(cls, name: str, locals: dict[Any, int], globals: dict[Any, int], instructions: list[Instruction]) -> CodeObject:
        return cls(_name=name, _locals=locals, _globals=globals, _instructions=instructions)

    @classmethod
    def builtints(cls, name: str) -> CodeObject:
        return cls(_name=name, _locals={}, _globals={}, _instructions=[])

    def __repr__(self) -> str:
        return f"<code object '{self._name}'>"
