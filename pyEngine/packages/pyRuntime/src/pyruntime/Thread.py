import json
from typing import Callable, Any
from dataclasses import dataclass

from pycompiler import Opcode, Instruction, Program
from .StackFrame import StackFrame
from .ThreadStatus import ThreadStatus

class Thread():
    def __init__(self, thread_id: int, program: Program, globals_dict: dict[str, Any], api_registry: dict[str, Callable]):

        self._thread_id: int = thread_id
        self._program: Program = program
        self._globals: dict[str, Any] = globals_dict
        self._api_registry: dict[str, Callable] = api_registry
        
        self._instruction_pointer: int = 0
        self._call_stack: list[StackFrame] = []

        self._status: ThreadStatus = ThreadStatus.RUNNABLE

        self.push_frame(return_address=-1)
    
    @property
    def id(self) -> int:
        return self._thread_id
        
    @property
    def current_frame(self) -> StackFrame:
        if not self._call_stack:
            raise RuntimeError(f"Thread {self._thread_id} has no active execution frames.")
        return self._call_stack[-1]
    
    @property
    def call_stack(self) -> list[StackFrame]:
        return self._call_stack

    @property
    def runnable(self) -> bool:
        return self._status == ThreadStatus.RUNNABLE
    
    @property
    def status(self) -> ThreadStatus:
        return self._status
    
    @property
    def globals(self) -> dict[str, Any]:
        return self._globals
    

    def push_frame(self, return_address: int) -> None:
        new_frame = StackFrame(return_address=return_address, globals_dict=self._globals)
        self._call_stack.append(new_frame)

    def step(self) -> ThreadStatus:
        if not self._call_stack: raise RuntimeError("Internal Error: VirtualThread should have attribute '_call_stack: list[StackFrame]'")
        if not self.runnable: return self.status
        if self._instruction_pointer >= len(self._program.instructions): 
            self._status = ThreadStatus.COMPLETED
            return self.status
        

        instruction: Instruction = self._program._instructions[self._instruction_pointer]
        self._instruction_pointer += 1

        self._execute_instruction(instruction.opcode, instruction.operand, self.current_frame)

        return self.status

    def __str__(self) -> str:
        return f"{self._program._instructions[self._instruction_pointer - 1]}: {self.current_frame}"

    def _execute_instruction(self, opcode: Opcode, operand: Any, stack_frame: StackFrame):

        match opcode:
            # --------------------------------------------------------------
            # Storage Operations
            # --------------------------------------------------------------
            case Opcode.LOAD_CONST: stack_frame.push_stack(operand)
            case Opcode.LOAD_GLOBAL: self.__load_global(operand, stack_frame)
            case Opcode.STORE_GLOBAL: stack_frame.globals[operand] = stack_frame.pop_stack()
            case Opcode.LOAD_LOCAL: self.__load_local(operand, stack_frame)
            case Opcode.STORE_LOCAL: stack_frame.locals[operand] = stack_frame.pop_stack()
            # --------------------------------------------------------------
            # Binary Math Operations
            # --------------------------------------------------------------
            case Opcode.BIN_ADD: self.__bin_op(opcode, stack_frame)
            case Opcode.BIN_SUB: self.__bin_op(opcode, stack_frame)
            case Opcode.BIN_MULT: self.__bin_op(opcode, stack_frame)
            case Opcode.BIN_DIV: self.__bin_op(opcode, stack_frame)
            # --------------------------------------------------------------
            # Life Cycle Operations
            # --------------------------------------------------------------
            case Opcode.POP_TOP: stack_frame.pop_stack()
            case Opcode.HALT: self._status = ThreadStatus.COMPLETED
            case _: raise RuntimeError("Could not match Opcode: {opcode}, to an operation.")


    def __load_global(self, operand: Any, stack_frame: StackFrame):
        if operand not in stack_frame.globals: raise NameError(f"Global name '{operand}' is not defined.")
        stack_frame.push_stack(stack_frame.globals[operand])

    def __load_local(self, operand: Any, stack_frame: StackFrame):
        if operand not in stack_frame.locals: raise NameError(f"Local name '{operand}' is not defined in this scope.")
        stack_frame.push_stack(stack_frame.locals[operand])

    def __bin_op(self, opcode: Opcode, stack_frame: StackFrame):

        match opcode:
            case Opcode.BIN_ADD:
                right = stack_frame.pop_stack()
                left = stack_frame.pop_stack()
                stack_frame.push_stack(left + right)
            case Opcode.BIN_SUB:
                right = stack_frame.pop_stack()
                left = stack_frame.pop_stack()
                stack_frame.push_stack(left - right)
            case Opcode.BIN_MULT:
                right = stack_frame.pop_stack()
                left = stack_frame.pop_stack()
                stack_frame.push_stack(left * right)
            case Opcode.BIN_DIV:
                right = stack_frame.pop_stack()
                left = stack_frame.pop_stack()
                stack_frame.push_stack(left / right)
            case _: raise RuntimeError("Could not match Opcode: {opcode}, to a binary operation.")
