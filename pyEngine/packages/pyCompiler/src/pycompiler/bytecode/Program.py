from __future__ import annotations


from dataclasses import dataclass
from typing import Iterable, TYPE_CHECKING

from .Instruction import Instruction

if TYPE_CHECKING:
    from .Opcode import Opcode


@dataclass(
    frozen=True,
    slots=True,
)
class Program:

    BYTECODE_VERSION = 1

    _instructions: tuple[Instruction, ..., ]


    @classmethod
    def of(cls, instructions: Iterable[Instruction]) -> Program:
        """
        Creates a program from the provided instructions.
        """
        immutable_instructions = tuple(instructions)

        return cls(immutable_instructions)

    @classmethod
    def of_binary(cls, binary: tuple[tuple[str, ...], ...]):
        return cls.of([Instruction.of_binary(binary_instruction) for binary_instruction in binary])


    def instruction_at(
        self,
        index: int,
    ) -> Instruction | None:
        """
        Returns the instruction at the requested index.

        Returns None when the index is outside the program.
        """

        if (
            index < 0
            or index >= len(
                self.instructions
            )
        ):
            return None

        return self.instructions[
            index
        ]

    @property
    def instructions(self) -> list[Instruction]:
        return self._instructions

    @property
    def opcodes(self) -> list[Opcode]:
        return [instruction.opcode for instruction in self.instructions]

    @property
    def binary(self) -> tuple[str, ...]:
        return tuple(instruction.binary for instruction in self.instructions)

    def __str__(self) -> str:

        output = "["

        for instruction in self.instructions:
            output += f"{instruction.__str__()}, "

        return output.strip(", ") + "]"