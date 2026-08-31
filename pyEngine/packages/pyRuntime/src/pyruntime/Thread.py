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
        """Executes a single Instruction. Returns False if halted or completed."""
        if not self._call_stack: raise RuntimeError("Internal Error: VirtualThread should have attribute '_call_stack: list[StackFrame]'")
        if not self.runnable: return self.status
        if self._instruction_pointer >= len(self._program.instructions): 
            self._status = ThreadStatus.COMPLETED
            return self.status
        

        instr: Instruction = self._program._instructions[self._instruction_pointer]
        self._instruction_pointer += 1

        frame = self.current_frame
        opcode = instr.opcode
        operand = instr.operand

        # --------------------------------------------------------------
        # Storage Operations
        # --------------------------------------------------------------
        if opcode == Opcode.LOAD_CONST:
            frame.push_stack(operand)

        elif opcode == Opcode.LOAD_GLOBAL:
            if operand not in frame.globals:
                raise NameError(f"Global name '{operand}' is not defined.")
            frame.push_stack(frame.globals[operand])

        elif opcode == Opcode.STORE_GLOBAL:
            frame.globals[operand] = frame.pop_stack()

        elif opcode == Opcode.LOAD_LOCAL:
            if operand not in frame.locals:
                raise NameError(f"Local name '{operand}' is not defined in this scope.")
            frame.push_stack(frame.locals[operand])

        elif opcode == Opcode.STORE_LOCAL:
            frame.locals[operand] = frame.pop_stack()

        # --------------------------------------------------------------
        # Binary Math Operations
        # --------------------------------------------------------------
        elif opcode == Opcode.BIN_ADD:
            right = frame.pop_stack()
            left = frame.pop_stack()
            frame.push_stack(left + right)

        elif opcode == Opcode.BIN_SUB:
            right = frame.pop_stack()
            left = frame.pop_stack()
            frame.push_stack(left - right)

        elif opcode == Opcode.BIN_MULT:
            right = frame.pop_stack()
            left = frame.pop_stack()
            frame.push_stack(left * right)

        elif opcode == Opcode.BIN_DIV:
            right = frame.pop_stack()
            left = frame.pop_stack()
            frame.push_stack(left / right)

        # # --------------------------------------------------------------
        # # Call Operations (Handling your ApiCall Dataclass)
        # # --------------------------------------------------------------
        # elif opcode == Opcode.CALL_API:
        #     api_call: ApiCall = operand
            
        #     # Resolve the registered Python host function
        #     if api_call.operation not in self.api_registry:
        #         raise RuntimeError(f"Unknown Game API operation: {api_call.operation}")
        #     func = self.api_registry[api_call.operation]

        #     # Collect arguments off the stack in reverse order
        #     args = []
        #     for _ in range(api_call.argument_count):
        #         args.insert(0, frame.pop())
            
        #     # Pop the receiver object (the entity performing the call, if applicable)
        #     receiver = frame.pop()

        #     # Invoke the underlying engine utility and push the result back
        #     result = func(receiver, *args)
        #     frame.push(result)

        # --------------------------------------------------------------
        # Life Cycle Operations
        # --------------------------------------------------------------
        elif opcode == Opcode.POP_TOP:
            frame.pop_stack()

        elif opcode == Opcode.HALT:
            self._status = ThreadStatus.COMPLETED
            return self.status

        return self.status

    def __str__(self) -> str:
        return f"{self._program._instructions[self._instruction_pointer - 1]}: {self.current_frame}"
