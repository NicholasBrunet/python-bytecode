from typing import Any
import json

class StackFrame:

    __next_stack_frame_id__ = 0

    def __init__(self, return_address: int, globals_dict: dict[int, Any]):

        self._stack_frame_id = self.__next_stack_frame_id__
        self._return_address = return_address
        self._operand_stack: list[Any] = []
        self._locals: dict[int, Any] = {}
        self._globals: dict[int, Any] = globals_dict

        self.__next_stack_frame_id__ += 1

    @property
    def id(self) -> int:
        return self._stack_frame_id
    
    @property
    def locals(self) -> dict[int, Any]:
        return self._locals
    
    @property
    def globals(self) -> dict[int, Any]:
        return self._globals
    
    @property
    def stack(self) -> list[Any]:
        return self._operand_stack

    def push_stack(self, value: Any) -> None:
        self._operand_stack.append(value)

    def pop_stack(self) -> Any:
        if not self._operand_stack:
            raise RuntimeError("Stack Underflow: Tried to pop from an empty operand stack!")
        return self._operand_stack.pop()

    def __str__(self) -> str:
        return json.dumps({
            "id": self.id,
            "stack": self.stack,
            "locals": self.locals,
            "globals": self.globals
        }, indent=4)
