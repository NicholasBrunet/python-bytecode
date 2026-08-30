from __future__ import annotations

from dataclasses import dataclass
from types import NoneType

from .Opcode import Opcode


# @dataclass(
#     frozen=True,
#     slots=True,
# )
# class ApiCall:
#     """
#     Describes a game API invocation performed by CALL_API.

#     Attributes:
#         operation:
#             Runtime operation identifier.

#         argument_count:
#             Number of arguments supplied to the operation, excluding
#             the receiver object.
#     """

#     operation: str
#     argument_count: int


#     def to_dict(self) -> dict[str, Any]:
#         """
#         Serializes this API call into a language-neutral representation.
#         """

#         return {
#             "operation": self.operation,
#             "argument_count": self.argument_count,
#         }


#     @classmethod
#     def from_dict(
#         cls,
#         data: dict[str, Any],
#     ) -> "ApiCall":
#         """
#         Creates an API call from its serialized representation.
#         """

#         operation = data.get(
#             "operation"
#         )

#         argument_count = data.get(
#             "argument_count"
#         )

#         if not isinstance(
#             operation,
#             str,
#         ):
#             raise ValueError(
#                 "ApiCall operation must be a string"
#             )

#         if not isinstance(
#             argument_count,
#             int,
#         ):
#             raise ValueError(
#                 "ApiCall argument_count must be an integer"
#             )

#         if argument_count < 0:
#             raise ValueError(
#                 "ApiCall argument_count cannot be negative"
#             )

#         return cls(
#             operation=operation,
#             argument_count=argument_count,
#       )


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
    def load_const(
        cls,
        value: object,
    ) -> Instruction:
        """
        Creates an instruction that loads a constant onto the stack.
        """

        return cls(
            Opcode.LOAD_CONST,
            value,
        )


    @classmethod
    def load_global(
        cls,
        name: str,
    ) -> Instruction:
        """
        Creates an instruction that loads a runtime global onto the stack.
        """

        return cls(
            Opcode.LOAD_GLOBAL,
            name,
        )


    @classmethod
    def store_global(
        cls,
        name: str,
    ) -> Instruction:
        """
        Creates an instruction that stores the top stack value globally.
        """

        return cls(
            Opcode.STORE_GLOBAL,
            name,
        )

    @classmethod
    def load_local(
        cls,
        name: str,
    ) -> Instruction:
        """
        Creates an instruction that loads a local variable onto the stack.
        """

        return cls(
            Opcode.LOAD_LOCAL,
            name,
        )


    @classmethod
    def store_local(
        cls,
        name: str,
    ) -> Instruction:
        """
        Creates an instruction that stores the top stack value locally.
        """

        return cls(
            Opcode.STORE_LOCAL,
            name,
        )


    # ------------------------------------------------------------------
    # Call Operations
    # ------------------------------------------------------------------

    # @classmethod
    # def call_api(
    #     cls,
    #     operation: str,
    #     argument_count: int = 0,
    # ) -> Instruction:
    #     """
    #     Creates an instruction that invokes a game API operation.
    #     """

    #     return cls(
    #         Opcode.CALL_API,
    #         ApiCall(
    #             operation=operation,
    #             argument_count=argument_count,
    #         ),
    #     )


    # ------------------------------------------------------------------
    # Life Cycle Operations
    # ------------------------------------------------------------------

    @classmethod
    def pop_top(cls) -> Instruction:
        """
        Creates an instruction that discards the top stack value.
        """

        return cls(
            Opcode.POP_TOP
        )

    @classmethod
    def duplicate_top(cls) -> Instruction:
        """
        Creates an instruction that duplicates the top stack value.
        """

        return cls(
            Opcode.DUO_TOP
        )


    @classmethod
    def halt(cls) -> Instruction:
        """
        Creates an instruction that stops execution.
        """

        return cls(
            Opcode.HALT
        )

    # ------------------------------------------------------------------
    # Binary Operations
    # ------------------------------------------------------------------

    @classmethod
    def binary_add(cls) -> Instruction:
        """
        Creates an instruction that adds stack[-2] and stack[-1]
        """

        return cls(
            Opcode.BIN_ADD
        )
    
    @classmethod
    def binary_subtract(cls) -> Instruction:
        """
        Creates an instruction that subtracts stack[-1] from stack[-2]
        """

        return cls(
            Opcode.BIN_SUB
        )
    
    @classmethod
    def binary_multiply(cls) -> Instruction:
        """
        Creates an instruction that multiplies stack[-2] by stack[-1]
        """

        return cls(
            Opcode.BIN_MULT
        )
    
    @classmethod
    def binary_divide(cls) -> Instruction:
        """
        Creates an instruction that divides stack[-2] by stack[-1]
        """

        return cls(
            Opcode.BIN_DIV
        )


    # ------------------------------------------------------------------
    # Class Properties
    # ------------------------------------------------------------------

    def __to_binary(self, operand: object) -> tuple[str, ...]:
        binary_list = []
        if isinstance(operand, int):
            # Prefix '0' means "this is a raw integer"
            binary_list.append(f"0{operand:08b}")
        elif isinstance(operand, str):
            # Prefix '1' means "this is a text character"
            for char in operand:
                binary_list.append(f"1{ord(char):08b}")
        elif isinstance(operand, NoneType):
            return self.__to_binary(255)
        return tuple(binary_list)

    @classmethod
    def __from_binary(self, binary_operand: tuple[str, ...]) -> object | None:

        decoded_chars = []
        for b_str in binary_operand:
            prefix = b_str[0]
            binary_val = b_str[1:]
            
            if prefix == "0":
                # It's a raw integer; parse it directly and return it
                if int(binary_val, 2) == 255: return None
                return int(binary_val, 2)
                
            elif prefix == "1":
                # It's a text character; decode it and collect it
                decoded_chars.append(chr(int(binary_val, 2)))
                
        # 2. If we collected text characters, join them back into a single string
        return "".join(decoded_chars) if decoded_chars else None

    @classmethod
    def of(cls, opcode: Opcode, operand: object | None = None) -> Instruction:
        """
        Creates a program from the provided instructions.
        """
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

    def __str__(self):
        return f"'{self.opcode.__str__()}', '{self.operand}'"