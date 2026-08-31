from dataclasses import dataclass, field
from typing import Any
from .Instruction import Instruction

@dataclass(frozen=True)
class CodeObject:
    """
    An immutable blueprint representing compiled code (a script, function, or method).
    Trapped inside constants tables until instantiated by the VM.
    """
    _storage_index: int
    _positional_argument_count: int
    _locals: dict[str, str]
    _instructions: list[Instruction]
    _constants: dict[str, str]
