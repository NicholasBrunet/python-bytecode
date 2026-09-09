import array
import time

from .server_constants import (MAX_LOGS)

class FastArrayLogger:
    __slots__ = ["timestamps", "core_ids", "ticks", "memories", "head", "is_full", "_cached_mem"]
    
    def __init__(self):
        self.timestamps = array.array('d', [0.0] * MAX_LOGS)
        self.core_ids = array.array('I', [0] * MAX_LOGS)
        self.ticks = array.array('I', [0] * MAX_LOGS)
        self.memories = array.array('d', [0.0] * MAX_LOGS)
        
        self.head = 0
        self.is_full = False
        self._cached_mem = 0.0

    def _get_linux_memory_mb(self) -> float:
        """
        Ultra-fast Linux memory reader. Bypasses the overhead of psutil
        by parsing the kernel's process stat file directly.
        """
        try:
            with open("/proc/self/statm", "r") as f:
                pages = int(f.read().split()[1])
                return (pages * 4096) / 1e6
        except Exception:
            return 0.0

    def log(self, core_id, clock_tick_count):
        if clock_tick_count % 50 == 0 or self._cached_mem == 0.0:
            self._cached_mem = self._get_linux_memory_mb()

        idx = self.head
        self.timestamps[idx] = time.time()
        self.core_ids[idx] = core_id
        self.ticks[idx] = clock_tick_count
        self.memories[idx] = self._cached_mem

        self.head += 1
        if self.head >= MAX_LOGS:
            self.head = 0
            self.is_full = True

    def dump(self):
        total_items = MAX_LOGS if self.is_full else self.head
        start_idx = self.head if self.is_full else 0
        
        for i in range(total_items):
            actual_index = (start_idx + i) % MAX_LOGS
            print(self.get_log_string(actual_index))

    def get_log_string(self, index):
        core_label = "Orchestrator" if self.core_ids[index] == 0 else f"Worker Core #{self.core_ids[index]}"
        return (f"[{self.timestamps[index]:.4f}] {core_label} | "
                f"Clock Tick: {self.ticks[index]} | {self.memories[index]:.2f} MB")
