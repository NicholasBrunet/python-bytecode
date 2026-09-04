from typing import Any, Self, TYPE_CHECKING
from dataclasses import dataclass, field

from .ThreadStatus import ThreadStatus
from .StackFrame import StackFrame

# if TYPE_CHECKING:
from .Thread import Thread

@dataclass
class ThreadPromise:

    _active_thread: Thread | None = None

    _final_id: int = field(default_factory=int)
    _final_status: ThreadStatus = ThreadStatus.RUNNABLE
    _final_globals: dict[str, Any] = field(default_factory=dict)
    _final_locals: dict[str, Any] = field(default_factory=dict)
    _error: Exception | None = None

    @classmethod
    def of(cls, thread: Thread) -> Self:
        return cls(_active_thread=thread)

    @property
    def id(self) -> int:
        if self._active_thread:
            return self._active_thread.id
        return self._final_id

    @property
    def status(self) -> ThreadStatus:
        if self._active_thread:
            return self._active_thread.status
        return self._final_status

    @property
    def thread(self) -> Thread | None:
        if self._active_thread != None: return self._active_thread


    def fulfill(self) -> None:
        if self._active_thread == None: return

        self._final_id = self._active_thread.id
        self._final_status = self._active_thread.status
        
        frame = self._active_thread.current_frame
        self._final_globals = dict(frame.globals)
        self._final_locals = dict(frame.locals)
            
        self._active_thread = None