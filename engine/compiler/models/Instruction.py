from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .Opcode import Opcode


@dataclass(
    frozen=True,
    slots=True,
)
class ApiCall:
    """
    Describes a game API invocation performed by CALL_API.

    Attributes:
        operation:
            Runtime operation identifier.

        argument_count:
            Number of arguments supplied to the operation, excluding
            the receiver object.
    """

    operation: str
    argument_count: int


    def to_dict(self) -> dict[str, Any]:
        """
        Serializes this API call into a language-neutral representation.
        """

        return {
            "operation": self.operation,
            "argument_count": self.argument_count,
        }


    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "ApiCall":
        """
        Creates an API call from its serialized representation.
        """

        operation = data.get(
            "operation"
        )

        argument_count = data.get(
            "argument_count"
        )

        if not isinstance(
            operation,
            str,
        ):
            raise ValueError(
                "ApiCall operation must be a string"
            )

        if not isinstance(
            argument_count,
            int,
        ):
            raise ValueError(
                "ApiCall argument_count must be an integer"
            )

        if argument_count < 0:
            raise ValueError(
                "ApiCall argument_count cannot be negative"
            )

        return cls(
            operation=operation,
            argument_count=argument_count,
        )


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

    opcode: Opcode
    operand: object | None = None


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

    @classmethod
    def call_api(
        cls,
        operation: str,
        argument_count: int = 0,
    ) -> Instruction:
        """
        Creates an instruction that invokes a game API operation.
        """

        return cls(
            Opcode.CALL_API,
            ApiCall(
                operation=operation,
                argument_count=argument_count,
            ),
        )


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
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """
        Serializes this instruction into a language-neutral dictionary.
        """

        operand = self.operand

        if isinstance(
            operand,
            ApiCall,
        ):
            operand = operand.to_dict()

        return {
            "opcode": self.opcode.value,
            "operand": operand,
        }


    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> Instruction:
        """
        Creates an instruction from its serialized representation.
        """

        raw_opcode = data.get(
            "opcode"
        )

        if not isinstance(
            raw_opcode,
            str,
        ):
            raise ValueError(
                "Instruction opcode must be a string"
            )

        try:
            opcode = Opcode(
                raw_opcode
            )

        except ValueError as error:
            raise ValueError(
                f"Unknown opcode: {raw_opcode}"
            ) from error

        operand = data.get(
            "operand"
        )

        if opcode is Opcode.CALL_API:

            if not isinstance(
                operand,
                dict,
            ):
                raise ValueError(
                    "CALL_API operand must be an object"
                )

            operand = ApiCall.from_dict(
                operand
            )

        return cls(
            opcode=opcode,
            operand=operand,
        )