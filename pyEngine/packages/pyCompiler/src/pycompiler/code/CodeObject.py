from dataclasses import dataclass, field
from typing import Any
from ..bytecode.Instruction import Instruction

@dataclass(frozen=True)
class CodeObject:
    """
    An immutable blueprint representing compiled code (a script, function, or method).
    Trapped inside constants tables until instantiated by the VM.
    """
    _locals: dict[Any, int] = field(default_factory=dict)
    _globals: dict[Any, int] = field(default_factory=dict)
    _constants: dict[Any, str] = field(default_factory=dict)
    _instructions: list[Instruction] = field(default_factory=list)
