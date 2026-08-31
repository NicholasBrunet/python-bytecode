from typing import Any, Callable, overload
from pycompiler.bytecode.Program import Program
from .Thread import Thread
from .ThreadStatus import ThreadStatus
from .ThreadPromise import ThreadPromise

class VirtualMachine:

    __next_virtual_machine_id__ = 0

    def __init__(self, api_registry: dict[str, Callable] | None = None):

        self._virtual_machine_id = VirtualMachine.__next_virtual_machine_id__
        self._programs: dict[int, Program] = {}
        self._programs_active: dict[int, int] = {} 
        self._virtual_threads: dict[int, Thread] = {}
        self._thread_promises: dict[int, ThreadPromise] = {}
        self._api_registry = api_registry or {}

        self._index_thread_program: dict[int, int] = {} # thread id to program id
        
        self._next_program_id = 0
        self._next_thread_id = 0

        VirtualMachine.__next_virtual_machine_id__ += 1

    @property
    def id(self) -> int:
        return self._virtual_machine_id



    @overload
    def program_id_of(self, thread: Thread) -> int | None: ...
    def _program_id_from_thread(self, thread: Thread) -> int | None:
        return self._index_thread_program.get(thread.id)

    @overload
    def program_id_of(self, program: Program) -> int | None: ...
    def _program_id_from_program(self, program: Program) -> int | None:
        for id, stored_program in self._programs.items():
            if stored_program == program: return id
        return None

    def program_id_of(self, *args):
        if isinstance(args[0], Thread): return self._program_id_from_thread(*args)
        elif isinstance(args[0], Program): return self._program_id_from_program(*args)



    def store_program(self, program: Program) -> int:
        program_id = self._next_program_id
        self._next_program_id += 1
        
        self._programs[program_id] = program
        return program_id

    def execute_program(self, program_id: int, initial_globals: dict[str, Any] | None = None) -> ThreadPromise:

        if program_id not in self._programs:
            raise KeyError(f"Cannot execute program with id: {program_id}, not found in VM program storage.")

        program = self._programs[program_id]
        thread_id = self._next_thread_id
        self._next_thread_id += 1

        globals_dict = initial_globals or {}

        if program_id in self._programs_active:
            raise ValueError(f"Program with id: {program_id} is being executed by virtual thread with id: {thread_id}")

        thread = Thread(
            thread_id=thread_id,
            program=program,
            globals_dict=globals_dict,
            api_registry=self._api_registry
        )

        thread_promise = ThreadPromise.of(thread)

        self._programs_active[program_id] = thread_id
        self._virtual_threads[thread_id] = thread
        self._thread_promises[thread_id] = thread_promise
        self._index_thread_program[thread_id] = program_id

        return thread_promise

    def tick(self) -> bool:

        thread_ids = list(self._virtual_threads.keys())
        
        for thread_id in thread_ids:

            thread = self._virtual_threads.get(thread_id)

            if not thread: continue
            if thread.runnable: status = thread.step()
            else: status = thread.status

            if status == ThreadStatus.COMPLETED:

                program_id = self.program_id_of(thread)
                thread_promise = self._thread_promises.get(thread_id)

                if program_id != None: self._programs_active.pop(program_id)
                if thread_promise != None: 
                    thread_promise.fulfill()
                    self._thread_promises.pop(thread_id)

                self._virtual_threads.pop(thread_id)
                self._index_thread_program.pop(thread_id)

        return len(self._virtual_threads) > 0