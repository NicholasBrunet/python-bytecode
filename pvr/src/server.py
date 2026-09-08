"""
when a user executes 'pypy3 -m pvr.server' it should boot up the runtime with a default of 2 cores
working, one being the Orchestrator and one being the worker for virtual runtimes, more cores can selected
for more workers for virtual runtimes.

by default you should not use a large amount of worker cores, each worker core can comfortably 
handle 100+ virtual runtimes across 1000's of virtual threads

Each core requires its own JIT interpretter resulting in a minimal overhead of a couple
dozen MB of RAM 
"""
import multiprocessing as mp
import multiprocessing.connection as mpc
import pypyjit
import gc
import time
import threading
import os
import signal

from .compiler import Compiler
from .server_constants import (
    DEFAULT_LOGGING_LEVEL,
    DEFAULT_WORKER_CLOCK_TICK_SPEED,
    DEFAULT_ORCHESTRATOR_CLOCK_TICK_SPEED,
    DEFAULT_WORKER_CORES,
    DEFAULT_RUNTIMES_PER_WORKER_CORE,
    MAX_WORKER_CORES,
    MAX_RUNTIMES_PER_WORKER_CORE,
    MAX_LOGS
)
from .utils import FastArrayLogger
from .worker import WorkerCore

import sys

MODULES_TO_STRIP = [
    'pdb', 'unittest', 'pydoc', 'email', 'http', 'urllib', 
    'xml', 'distutils', 'ctypes', 'logging'
]

for mod in MODULES_TO_STRIP:
    if mod in sys.modules:
        del sys.modules[mod]


class WorkerConnection:

    __slots__: list[str] = ["worker_process", "orchestrator_connection"]
    def __init__(self,
                 worker_process: mp.Process | None = None,
                 orchestrator_connection: mpc.Connection | None = None):
        self.worker_process = worker_process
        self.orchestrator_connection = orchestrator_connection


class Orchestrator:
    """
    Main handler for distributing worker cores and handling their executions.
    """

    __slots__: list[str] = ["worker_cores", "worker_connections", "runtimes_per_core", "logger"]
    def __init__(self, 
                 worker_cores: int = DEFAULT_WORKER_CORES, 
                 runtimes_per_core: int = DEFAULT_RUNTIMES_PER_WORKER_CORE):

        self.worker_cores: int = worker_cores
        self.runtimes_per_core: int = runtimes_per_core

        self.worker_connections: list[WorkerConnection] = [WorkerConnection() for _ in range(worker_cores)]
        self.logger = FastArrayLogger()

    def _interactive_shell(self):
        """
        Runs in a background thread to handle user commands without blocking the core clock.
        """
        print("\n--- PVR Shell Active (Type 'help' for commands) ---")
        while True:
            try:
                cmd = input("pvr> ").strip().lower()
                if not cmd:
                    continue

                if cmd == "help":
                    print("Available commands:")
                    print("  status : View current orchestrator tick status")
                    print("  stats  : View pypyjit information of orchestrator")
                    print("  logs   : Instantly dump current orchestrator array logs")
                    print("  exit   : Trigger a clean system shutdown sequence")

                elif cmd == "stats":
                    print("\n[PyPy Core JIT & Memory Diagnostics]")

                    total_allocated, memory_in_use = pypyjit.get_stats_asmmemmgr()
                    print(f"  JIT Backend Raw Allocation: {total_allocated / 1e6:.2f} MB")
                    print(f"  JIT Backend Memory in Use : {memory_in_use / 1e6:.2f} MB")

                    gc_data = gc.get_stats(memory_pressure=True)
                    print("\n[GC Arena Insights]")
                    print(f"  {gc_data}")
                
                elif cmd == "status":
                    print(f"[Status] Active Worker Cores: {self.worker_cores}")
                    print(f"[Status] Orchestrator Logs Recorded: {len(self.logger.core_ids)}")
                
                elif cmd == "logs":

                    print("\n--- Snapshot of Current Worker Logs ---")

                    for worker_connection in self.worker_connections:
                        worker_process = worker_connection.worker_process
                        if worker_process and worker_process.is_alive():
                            os.kill(worker_process.pid, signal.SIGUSR1)
                        time.sleep(0.1)

                    print("\n--- Snapshot of Current Orchestrator Logs ---")

                    self.logger.dump()

                    print("--------------------------------------------")
                
                elif cmd == "exit":
                    print("[Shell] Shutdown requested via CLI.")
                    os.kill(os.getpid(), signal.SIGINT)
                    break
                else:
                    print(f"Unknown command: '{cmd}'. Type 'help' for options.")
                    
            except (EOFError, KeyboardInterrupt):
                break

    def start(self):
        """
        Registers worker processes and begins main orchestration clock
        """

        for worker_core_id in range(self.worker_cores):

            orchestrator_connection, worker_connection = mp.Pipe()
            worker_core = WorkerCore(worker_core_id, worker_connection, self.runtimes_per_core)

            worker_process = mp.Process(target=worker_core.start)
            worker_process.start()

            self.worker_connections[worker_core_id].worker_process = worker_process
            self.worker_connections[worker_core_id].orchestrator_connection = orchestrator_connection

        shell_thread = threading.Thread(target=self._interactive_shell, daemon=True)
        shell_thread.start()

        try:
            clock_tick_count = 0
            while True:
                self.logger.log(0, clock_tick_count)
                time.sleep(DEFAULT_ORCHESTRATOR_CLOCK_TICK_SPEED)
                clock_tick_count += 1
        except (Exception, KeyboardInterrupt) as e:
            pass
        finally:
            print("\n[Orchestrator] Initiating system shutdown sequence...")
            for worker_connection in self.worker_connections:
                worker_process = worker_connection.worker_process
                if worker_process.is_alive():
                    os.kill(worker_process.pid, signal.SIGUSR1)
                    worker_process.join(timeout=1.0)

            if DEFAULT_LOGGING_LEVEL >= 1:
                print("\n--- Dumping Orchestrator Logs ---")
                self.logger.dump()

            self.worker_connections = [[None, None] for _ in range(self.worker_cores)]
            
            print("\nShutdown successful.")

if __name__ == "__main__":
    if DEFAULT_WORKER_CORES > MAX_WORKER_CORES:
        raise RuntimeError("Cannot start server in this environment. Requires 2 CPU cores minimum.")

    orchestrator = Orchestrator()
    orchestrator.start()