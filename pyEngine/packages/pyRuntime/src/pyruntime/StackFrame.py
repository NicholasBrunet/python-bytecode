from typing import Any

class StackFrame:
    def __init__(self, return_address: int, globals_dict: dict[int, Any]):

        self._return_address = return_address
        self._operand_stack: list[Any] = []
        self._locals: dict[int, Any] = {}
        self._globals: dict[int, Any] = globals_dict

    def push_stack(self, value: Any) -> None:
        self._operand_stack.append(value)

    def pop_stack(self) -> Any:
        if not self._operand_stack:
            raise RuntimeError("Stack Underflow: Tried to pop from an empty operand stack!")
        return self._operand_stack.pop()
