import psutil
import os
import time

class BenchmarkMonitor:
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        
    def start(self):
        """Captures the baseline state of CPU and Disk I/O."""
        self.start_time = time.perf_counter()
        self.cpu_start = self.process.cpu_times()
        self.io_start = self.process.io_counters()

    def stop(self):
        """Calculates the difference and prints a clean report."""
        duration = time.perf_counter() - self.start_time
        cpu_end = self.process.cpu_times()
        io_end = self.process.io_counters()

        # Calculate deltas (Changes)
        user_cpu = cpu_end.user - self.cpu_start.user
        sys_cpu = cpu_end.system - self.cpu_start.system
        read_mb = (io_end.read_bytes - self.io_start.read_bytes) / (1024**2)
        write_mb = (io_end.write_bytes - self.io_start.write_bytes) / (1024**2)

        print("\n" + "="*35)
        print("  RESOURCE UTILIZATION REPORT")
        print("="*35)
        print(f"Total Wall Time : {duration:.4f} s")
        print(f"User CPU Time   : {user_cpu:.4f} s (Logic)")
        print(f"System CPU Time : {sys_cpu:.4f} s (I/O/Kernel)")
        print(f"Disk Read       : {read_mb:.2f} MB")
        print(f"Disk Write      : {write_mb:.2f} MB")
        print("="*35 + "\n")