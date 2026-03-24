# logger.py

class Logger:
    def __init__(self):
        self.logs = []   # stores every event as a list, useful for a summary at the end

    def _log(self, time, message):
        entry = f"[t={time:>3}] {message}"
        self.logs.append(entry)
        print(entry)

    # --- Scheduling events ---
    def process_arrived(self, time, pcb):
        self._log(time, f"Process {pcb.pid} arrived → NEW to READY")

    def process_selected(self, time, pcb):
        self._log(time, f"Scheduler selected Process {pcb.pid} → RUNNING (remaining burst: {pcb.remaining_time})")

    def process_preempted(self, time, pcb):
        self._log(time, f"Process {pcb.pid} preempted → READY (remaining burst: {pcb.remaining_time})")

    def process_terminated(self, time, pcb):
        self._log(time, f"Process {pcb.pid} finished → TERMINATED "
                        f"(turnaround: {pcb.turnaround_time}, waiting: {pcb.waiting_time})")

    # --- Memory events ---
    def memory_allocated(self, time, pcb):
        self._log(time, f"Memory allocated for Process {pcb.pid} "
                        f"({pcb.memory_required} units at address {pcb.memory_address})")

    def memory_released(self, time, pcb):
        self._log(time, f"Memory released for Process {pcb.pid} ({pcb.memory_required} units freed)")

    def memory_denied(self, time, pcb):
        self._log(time, f"Process {pcb.pid} waiting — insufficient memory "
                        f"({pcb.memory_required} units requested)")

    # --- Resource events ---
    def resource_acquired(self, time, pcb, resource_name):
        self._log(time, f"Process {pcb.pid} acquired '{resource_name}'")

    def resource_released(self, time, pcb, resource_name):
        self._log(time, f"Process {pcb.pid} released '{resource_name}'")

    def resource_blocked(self, time, pcb, resource_name):
        self._log(time, f"Process {pcb.pid} blocked → WAITING (resource '{resource_name}' is busy)")

    def resource_unblocked(self, time, pcb, resource_name):
        self._log(time, f"Process {pcb.pid} unblocked → READY (resource '{resource_name}' now available)")

    # --- Summary at the end ---
    def print_summary(self):
        print("\n" + "="*50)
        print("SIMULATION COMPLETE — FULL LOG")
        print("="*50)
        for entry in self.logs:
            print(entry)