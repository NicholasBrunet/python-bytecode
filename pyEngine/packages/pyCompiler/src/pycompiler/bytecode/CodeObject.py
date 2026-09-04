from __future__ import annotations

import ast
from dataclasses import dataclass, field
import json
from typing import Any

from .Instruction import Instruction

@dataclass(frozen=True)
class CodeObject:
    """
    An immutable blueprint representing compiled code (a script, function, or method).
    Trapped inside constants tables until instantiated by the VM.
    """
    _name: str = ""
    _locals: list[Any] = field(default_factory=list)
    _globals: dict[Any, int] = field(default_factory=dict)
    _constants: dict[Any, Any] = field(default_factory=dict)
    _instructions: list[Instruction] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self._name

    @property
    def locals(self) -> list[Any]:
        return self._locals

    @property
    def globals(self) -> dict[Any, int]:
        return self._globals

    @property
    def constants(self) -> dict[Any, Any]:
        return self._constants
    
    @property
    def instructions(self) -> list[Instruction]:
        return self._instructions

    @classmethod
    def new(cls, name: str, locals: list[Any], globals: dict[Any, int], constants: dict[Any, Any], instructions: list[Instruction]) -> CodeObject:
        return cls(_name=name, _locals=locals, _globals=globals, _constants=constants, _instructions=instructions)

    @classmethod
    def builtints(cls, name: str) -> CodeObject:
        return cls(_name=name, _locals=[], _globals={}, _constants={}, _instructions=[])

    def to_dict(self) -> dict[str, Any]:
        clean_constants = {}
        for key, val in self._constants.items():
            if isinstance(val, CodeObject): clean_constants[key] = val.to_dict()
            else: clean_constants[key] = val

        return {'code object': {
            "name": self._name,
            "locals": self._locals,
            "globals": self._globals,
            "constants": clean_constants,
            "instructions": [instruction.__repr__() for instruction in self._instructions]
        }}

    def __repr__(self) -> str:

        return json.dumps(self.to_dict(), indent=4)

    def __str__(self) -> str:
        return f"<code object '{self.name}'>"

