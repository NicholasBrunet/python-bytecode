from typing import Any, Callable
from pycompiler.bytecode.Program import Program
from pyruntime.VirtualThread import VirtualThread

class VirtualMachine:

    __next_virtual_machine_id__ = 0

    def __init__(self, api_registry: dict[str, Callable] | None = None):

        self._virtual_machine_id = VirtualMachine.__next_virtual_machine_id__
        self._programs: dict[int, Program] = {}
        self._programs_active: dict[int, int] = {} 
        self._virtual_threads: dict[int, VirtualThread] = {}
        self._api_registry = api_registry or {}
        
        self._next_program_id = 0
        self._next_thread_id = 0

        VirtualMachine.__next_virtual_machine_id__ += 1

    def store_program(self, program: Program) -> int:
        program_id = self._next_program_id
        self._next_program_id += 1
        
        self._programs[program_id] = program
        return program_id

    def execute_program(self, program_id: int, initial_globals: dict[str, Any] | None = None) -> int:

        if program_id not in self._programs:
            raise KeyError(f"Cannot execute program: Program ID {program_id} not found in VM storage.")

        program = self._programs[program_id]
        thread_id = self._next_thread_id
        self._next_thread_id += 1

        globals_dict = initial_globals or {}

        if program_id in self._programs_active:
            raise ValueError(f"Program with id: {program_id} is being executed by virtual thread with id: {thread_id}")

        new_thread = VirtualThread(
            thread_id=thread_id,
            program=program,
            globals_dict=globals_dict,
            api_registry=self._api_registry
        )

        self._virtual_threads[thread_id] = new_thread
        self._programs_active[program_id] = thread_id

        # START OF THREAD EXECUTION

        # END OF THREAD EXECUTION

        self._programs_active.pop(program_id)

        return thread_id