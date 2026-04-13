# cpu.py

class CPU:

    speed = 1 #1 to 1 with system clock when using % operator

    def __init__(self):
        self.is_busy = False
        self.held_by = None  # stores the pid of the current process

    def acquire(self, pcb):
        self.is_busy = True
        self.held_by = pcb.pid
        pcb.waiting_for = None

    def release(self):
        self.is_busy = False
        self.held_by = None