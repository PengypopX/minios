# scheduler.py

from collections import deque
from pcb import State
from resource_manager_v2 import CPU

class Scheduler:
    def __init__(self, policy, quantum=2):
        self.policy       = policy.upper()
        self.quantum      = quantum
        self.ready_queue  = deque()          # all READY processes waiting for CPU

    # --- Add a process to the ready queue ---
    def add_process(self, pcb):
        pcb.state = State.READY
        self.ready_queue.append(pcb)

    # --- Select the next process to run ---
    def select_next(self):
        if not self.ready_queue: #QUEUE IS EMPTY
            return None   # nothing to run
        if self.policy == "FCFS":
            return self._fcfs()
        elif self.policy == "RR":
            return self._rr()
        elif self.policy == "SJF":
            return self._sjf()
        else:
            raise ValueError(f"Unknown policy: {self.policy}")

    # --- Tick the current process (called every time unit) ---
    def tick(self, current_pcb, logger, time):
        if current_pcb is None:
            return None

        current_pcb.remaining_time -= 1
        current_pcb.quantum_elapsed += 1

        # Check if process is done
        if current_pcb.remaining_time <= 0:
            current_pcb.state = State.TERMINATED
            current_pcb.finish_time = time + 1
            current_pcb.quantum_elapsed = 0
            logger.process_terminated(time, current_pcb)
            return "terminated"

        if self.policy == "RR" and current_pcb.quantum_elapsed >= self.quantum:
            current_pcb.state = State.READY
            current_pcb.quantum_elapsed = 0
            self.ready_queue.append(current_pcb)
            logger.process_preempted(time, current_pcb)
            return "preempted"

        return "running"

    # --------------------------------------------------
    # Private policy implementations
    # --------------------------------------------------

    def _fcfs(self):
        # Just take whoever has been waiting longest (front of queue)
        return self.ready_queue.popleft()

    def _rr(self):
        # Same as FCFS for selection — the quantum logic is in tick()
        return self.ready_queue.popleft()

    def _sjf(self):
        # Pick the process with the shortest TOTAL burst time
        shortest = min(self.ready_queue, key=lambda p: p.burst_time)
        self.ready_queue.remove(shortest)
        return shortest
    
    def _io_sjf(self, blocked_queue):
        if not blocked_queue:
            return None
        shortest_io = min(blocked_queue,key= lambda p: p.io_request_size)
        blocked_queue.remove(shortest_io)
        return shortest_io
    