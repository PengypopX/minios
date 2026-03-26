# scheduler.py

from collections import deque
from pcb import State

class Scheduler:
    def __init__(self, policy, quantum=2):
        self.policy       = policy.upper()   # "FCFS", "RR", or "SJF"
        self.quantum      = quantum          # only used by Round Robin
        self.ready_queue  = deque()          # all READY processes waiting for CPU
        self.time_on_cpu  = 0               # tracks how long current process has been running (RR)

    # --- Add a process to the ready queue ---
    def add_process(self, pcb):
        pcb.state = State.READY
        self.ready_queue.append(pcb)

    # --- Select the next process to run ---
    def select_next(self):
        if not self.ready_queue:
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
        self.time_on_cpu += 1

        # Check if process is done
        if current_pcb.remaining_time <= 0:
            current_pcb.state       = State.TERMINATED
            current_pcb.finish_time = time + 1
            self.time_on_cpu        = 0
            logger.process_terminated(time, current_pcb)
            return "terminated"

        # Check if Round Robin quantum is exhausted
        if self.policy == "RR" and self.time_on_cpu >= self.quantum:
            current_pcb.state = State.READY
            self.ready_queue.append(current_pcb)
            self.time_on_cpu  = 0
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