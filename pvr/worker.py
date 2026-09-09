import time
import signal
import pypyjit
import gc
from multiprocessing import connection as mpc

from .utils import FastArrayLogger
from .server_constants import (
    DEFAULT_RUNTIMES_PER_WORKER_CORE,
    DEFAULT_LOGGING_LEVEL,
    DEFAULT_WORKER_CLOCK_TICK_SPEED
)

class WorkerCore:
    """
    Controls multiple Virtual Runtimes on one dedicated CPU core
    """

    __slots__: list[str] = ["worker_id", "worker_connection", "virtual_runtimes", "logger"]
    def __init__(self, 
                 worker_id: int,
                 worker_connection: mpc.Connection,
                 runtimes: int = DEFAULT_RUNTIMES_PER_WORKER_CORE):

        self.worker_id: int = worker_id
        self.worker_connection: mpc.Connection = worker_connection
        self.virtual_runtimes: list = [None] * runtimes
        self.logger = FastArrayLogger()

    def _signal_dump_handler(self, signum, frame):
        """
        Asynchronously intercepts execution to safely print log frames
        """
        gc.enable()
        print(f"\n--- Live Signal Dump: Worker Core #{self.worker_id + 1} ---")
        self.logger.dump()
        gc.collect()
        gc.disable()

    def check_poll(self, value: object) -> bool:
        if self.worker_connection.poll(): 
            if self.worker_connection.recv() == value:
                return True
        return False

    def start(self):
        """
        Begins Worker Core clock
        """

        pypyjit.set_param("threshold=20")
        pypyjit.set_param("trace_eagerness=10")

        signal.signal(signal.SIGUSR1, self._signal_dump_handler)
        gc.disable()

        try:
            clock_tick_count = 0
            while True:
                self.logger.log(self.worker_id + 1, clock_tick_count)
                time.sleep(DEFAULT_WORKER_CLOCK_TICK_SPEED)
                clock_tick_count += 1
        except KeyboardInterrupt:
            pass
        finally:
            gc.enable()