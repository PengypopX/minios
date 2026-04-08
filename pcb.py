# pcb.py

from enum import Enum

class State(Enum):
    NEW        = "NEW"
    READY      = "READY"
    RUNNING    = "RUNNING"
    BLOCKED    = "BLOCKED"
    TERMINATED = "TERMINATED"

class PCB:
    def __init__(self, pid, arrival_time, burst_time, memory_required, priority=0):
        # --- Identity ---
        self.pid              = pid             # Unique integer ID
        self.priority         = priority        # Used if you pick Priority scheduling

        # --- Time tracking ---
        self.arrival_time     = arrival_time    # When the job enters the system
        self.burst_time       = burst_time      # Total CPU time it needs
        self.remaining_time   = burst_time      # Counts down as it runs (used by RR / SRTF)
        self.start_time       = None            # Set the first time it enters RUNNING
        self.finish_time      = None            # Set when it hits TERMINATED

        # --- Memory ---
        self.memory_required  = memory_required # How many memory units it needs
        self.memory_address   = None            # Where in memory it was allocated (set by memory manager)

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
        