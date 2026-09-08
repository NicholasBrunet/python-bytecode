"""
Python virtual Runtime managed in a single process
"""

from __future__ import annotations
from itertools import count

from .code import CodeObject
from .constants import (
    MAX_VTHREADS, 
    MAX_VSTORAGE_GLOBALS, 
    MAX_VSTORAGE_CONSTANTS, 
    MAX_VFRAME_LOCALS, 
    MAX_VFRAME_EVALUATION_STACK
)

thread_id_generator = count()
def next_thread_id() -> int:
    return next(thread_id_generator)

class VThread:
    """
    TODO
    """

    __slots__ = ["thread_id", "runtime", "instruction_counter", "code_object", "frame", "is_alive"]
    def __init__(self, thread_id: int, runtime: VRuntime):

        self.thread_id: int = thread_id

        self.runtime = runtime
        self.instruction_counter: int = 0
        self.code_object: CodeObject | None = None
        self.frame: VFrame | None = None

        self.is_alive: bool = False

class VFrame:
    """
    TODO
    """

    __slots__ = ["parent_frame", "locals", "evaluation_stack"]
    def __init__(self, parent_frame: VFrame | None = None):
        self.parent_frame: VFrame | None = parent_frame

        self.locals: list[object | None] = [None] * MAX_VFRAME_LOCALS
        self.evaluation_stack: list[object | None] = [None] * MAX_VFRAME_EVALUATION_STACK

class VStorage:
    """
    TODO
    """

    __slots__ = ["_heap_globals", "_heap_constants"]
    def __init__(self):

        self._heap_globals: list[object | None] = [None] * MAX_VSTORAGE_GLOBALS
        self._heap_constants: list[object | None] = [None] * MAX_VSTORAGE_CONSTANTS

class VRuntime:
    """
    Virtualized runtime responsible for running python byte code
    across virtualized threads

    IF AN UNCAUGHT ERROR HAPPENS IN ONE RUNTIME IT
    MAY KILL THE ENTIRE WORKER CORE...
    """

    __slots__ = ["threads", "storage", "active_threads"]
    def __init__(self):
        self.threads: list[VThread] = [VThread(next_thread_id(), self) for _ in range(MAX_VTHREADS)]
        self.storage: VStorage = VStorage()

        self.active_threads: VThread | None = [None] * MAX_VTHREADS