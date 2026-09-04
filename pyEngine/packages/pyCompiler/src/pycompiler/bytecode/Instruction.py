from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from types import NoneType

from .Opcode import Opcode


@dataclass(
    frozen=True,
    slots=True,
)
class Instruction:
    """
    Represents a single bytecode instruction.

    Instructions can be serialized into a language-neutral format for
    transmission between the compiler, web server, and game runtimes.
    """

    _opcode: Opcode
    _operand: object | None = None


    # ------------------------------------------------------------------
    # Storage Operations
    # ------------------------------------------------------------------

    @classmethod
    def load_const(cls, value: object) -> Instruction:
        return cls(Opcode.LOAD_CONST, value)

    @classmethod
    def load_name(cls, storage_index: int) -> Instruction:
        return cls(Opcode.LOAD_NAME, storage_index)

    @classmethod
    def store_name(cls, storage_index: int) -> Instruction:
        return cls(Opcode.STORE_NAME, storage_index)

    @classmethod
    def load_fast(cls, storage_index: int) -> Instruction:
        return cls(Opcode.LOAD_FAST, storage_index)

    @classmethod
    def store_fast(cls, storage_index: int) -> Instruction:
        return cls(Opcode.STORE_FAST, storage_index)

    # ------------------------------------------------------------------
    # Life Cycle Operations
    # ------------------------------------------------------------------

    @classmethod
    def make_function(cls) -> Instruction:
        return cls(Opcode.MAKE_FUNCTION)
    
    @classmethod
    def call(cls, argument_count: int) -> Instruction:
        return cls(Opcode.CALL, argument_count)
    
    @classmethod
    def return_value(cls) -> Instruction:
        return cls(Opcode.RETURN_VALUE)

    @classmethod
    def pop_jump_if_false(cls, jump_amount: int) -> Instruction:
        return cls(Opcode.POP_JUMP_IF_FALSE, jump_amount)

    @classmethod
    def push_null(cls) -> Instruction:
        return cls(Opcode.PUSH_NULL)

    @classmethod
    def pop_top(cls) -> Instruction:
        return cls(Opcode.POP_TOP)

    @classmethod
    def duplicate_top(cls) -> Instruction:
        return cls(Opcode.DUO_TOP)

    @classmethod
    def swap(cls, stack_index: int) -> Instruction:
        return cls.of(Opcode.SWAP, stack_index)
    
    @classmethod
    def halt(cls) -> Instruction:
        return cls(Opcode.HALT)

    # ------------------------------------------------------------------
    # Comparison Operations
    # ------------------------------------------------------------------

    @classmethod
    def compare_op(cls, operator_code: int) -> Instruction:
        return cls.of(Opcode.COMPARE_OP, operator_code)
    
    # ------------------------------------------------------------------
    # Binary Operations
    # ------------------------------------------------------------------

    @classmethod
    def binary_add(cls) -> Instruction:
        return cls(Opcode.BIN_ADD)
    
    @classmethod
    def binary_subtract(cls) -> Instruction:
        return cls(Opcode.BIN_SUB)
    
    @classmethod
    def binary_multiply(cls) -> Instruction:
        return cls(Opcode.BIN_MULT)
    
    @classmethod
    def binary_divide(cls) -> Instruction:
        return cls(Opcode.BIN_DIV)

    # ------------------------------------------------------------------
    # Class Properties
    # ------------------------------------------------------------------

    # def __to_binary(self, operand: object) -> tuple[str, ...]:
    #     binary_list = []
    #     if isinstance(operand, int):
    #         # Prefix '0' means "this is a raw integer"
    #         binary_list.append(f"0{operand:08b}")
    #     elif isinstance(operand, str):
    #         # Prefix '1' means "this is a text character"
    #         for char in operand:
    #             binary_list.append(f"1{ord(char):08b}")
    #     elif isinstance(operand, NoneType):
    #         return self.__to_binary(255)
    #     return tuple(binary_list)

    # @classmethod
    # def __from_binary(cls, binary_operand: tuple[str, ...]) -> object | None:

    #     decoded_chars = []
    #     for b_str in binary_operand:
    #         prefix = b_str[0]
    #         binary_val = b_str[1:]
            
    #         if prefix == "0":
    #             # It's a raw integer; parse it directly and return it
    #             if int(binary_val, 2) == 255: return None
    #             return int(binary_val, 2)
                
    #         elif prefix == "1":
    #             # It's a text character; decode it and collect it
    #             decoded_chars.append(chr(int(binary_val, 2)))
                
    #     # 2. If we collected text characters, join them back into a single string
    #     return "".join(decoded_chars) if decoded_chars else None

    @classmethod
    def of(cls, opcode: Opcode, operand: object | None = None) -> Instruction:
        return cls(opcode, operand)

    @classmethod
    def of_binary(cls, binary_instruction: tuple[str, ...]) -> Opcode:
        return cls(Opcode.of_binary(binary_instruction[0]), cls.__from_binary(binary_instruction[1:]))


    @property
    def opcode(self) -> Opcode:
        return self._opcode
    
    @property
    def operand(self) -> object | None:
        return self._operand

    @property
    def binary(self) -> tuple[str, ...]:
        return (self.opcode.value, *self.__to_binary(self.operand))

    def __repr__(self):
        return f"{self.opcode} {self.operand}"