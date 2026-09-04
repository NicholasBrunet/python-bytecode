from enum import Enum, auto

class ThreadStatus(Enum):
    RUNNABLE = auto()
    BLOCKED = auto()
    COMPLETED = auto()