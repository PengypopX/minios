# memory_manager.py

class MemoryManager:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.allocated_blocks = []  # list of (start_address, size, pid)

    # --- How much memory is currently free ---
    def available_memory(self):
        used = sum(size for _, size, _ in self.allocated_blocks)
        return self.total_memory - used

    # --- Try to allocate memory for a process ---
    def allocate(self, pcb):
        if pcb.memory_required > self.total_memory:
            raise ValueError(f"Process {pcb.pid} needs more memory than the system has total.")

        # Sort blocks by start address so we can scan gaps left to right
        self.allocated_blocks.sort(key=lambda b: b[0])

        # Build a list of occupied ranges and look for a gap big enough
        address = 0
        for (start, size, pid) in self.allocated_blocks:
            gap = start - address
            if gap >= pcb.memory_required:
                # Found a gap — allocate here
                return self._place(pcb, address)
            address = start + size

        # Check the space after the last block
        if self.total_memory - address >= pcb.memory_required:
            return self._place(pcb, address)

        # No gap was big enough
        return False

    # --- Actually place the block and update the PCB ---
    def _place(self, pcb, address):
        self.allocated_blocks.append((address, pcb.memory_required, pcb.pid))
        pcb.memory_address = address
        return True

    # --- Release memory when a process terminates ---
    def release(self, pcb):
        self.allocated_blocks = [
            b for b in self.allocated_blocks if b[2] != pcb.pid
        ]
        pcb.memory_address = None