# pcb.py

from enum import Enum

class State(Enum):
    NEW        = "NEW"
    READY      = "READY"
    RUNNING    = "RUNNING"
    BLOCKED    = "BLOCKED"
    TERMINATED = "TERMINATED"

#CHANGES NEEDED = MORE REALISTIC TIME (some ms)
#BETTER USAGE OF BLOCKED STATE
#WAIT QUEUE

class PCB:
    def __init__(self, pid, arrival_time, burst_time, memory_required, priority=0):
        # --- Identity ---
        self.pid              = pid             # Unique integer ID
        self.priority         = priority        # Used if you pick Priority scheduling

        # Parameters CPU will use during context switching (timing)
        self.arrival_time     = arrival_time    # C
        self.burst_time       = burst_time      # Burst time is total time integer needed for process to enter termination state
        self.remaining_time   = burst_time
        self.start_time       = None
        self.finish_time      = None

        self.quantum_elapsed = 0 #used in scheduler.py to track time slices used
        # --- Memory ---
        self.memory_required  = memory_required # How much memory the program wants
        self.memory_address   = None            # Virtual memory, CPU tracks hard coded memory!

        # --- State ---
        self.state            = State.NEW       # Starts as NEW, transitions from there

        # --- Resource tracking ---
        self.waiting_for      = None            # Name of the resource it's blocked on, if any
        self.open_files = []
        self.io_request_size = 0
        self.needs_resource = None   # tuple of (resource_name, tick_to_request) or None
        self.resource_acquired = False

    # --- Computed stats (useful for your logs at the end) ---
    @property
    def turnaround_time(self):
        if self.finish_time is not None:
            return self.finish_time - self.arrival_time
        return None

    @property
    def waiting_time(self):
        if self.turnaround_time is not None:
            return self.turnaround_time - self.burst_time
        return None

    #allows for print(process in a formatted string)
    def __repr__(self):
        return (f"PCB(pid={self.pid}, state={self.state.value}, "
                f"remaining={self.remaining_time}, mem={self.memory_required})")
    
    def add_file(self, file_name):
        if file_name not in self.open_files:
            self.open_files.append(file_name)
    
    def request_io(self, size):
        self.io_request_size = size
        self.state = State.BLOCKED
        self.waiting_for = "I/O"
        