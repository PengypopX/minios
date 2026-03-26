# resource_manager.py

from collections import deque

class Resource:
    def __init__(self, name):
        self.name       = name
        self.is_busy    = False       # is someone currently using it?
        self.held_by    = None        # which pid is holding it right now
        self.wait_queue = deque()     # processes waiting for it, in order

    def __repr__(self):
        return f"Resource(name={self.name}, busy={self.is_busy}, held_by={self.held_by})"


class ResourceManager:
    def __init__(self):
        self.resources = {}   # name → Resource object

    # --- Register a resource into the system ---
    def add_resource(self, name):
        self.resources[name] = Resource(name)

    # --- Try to acquire a resource ---
    def acquire(self, pcb, resource_name, logger, time):
        resource = self.resources[resource_name]

        if not resource.is_busy:
            # Resource is free — give it to the process
            resource.is_busy = True
            resource.held_by = pcb.pid
            pcb.waiting_for  = None
            logger.resource_acquired(time, pcb, resource_name)
            return True
        else:
            # Resource is busy — block the process
            resource.wait_queue.append(pcb)
            pcb.waiting_for = resource_name
            logger.resource_blocked(time, pcb, resource_name)
            return False

    # --- Release a resource ---
    def release(self, pcb, resource_name, logger, time):
        resource = self.resources[resource_name]

        resource.is_busy = False
        resource.held_by = None
        logger.resource_released(time, pcb, resource_name)

        # If anyone is waiting, unblock the next one in line
        if resource.wait_queue:
            next_pcb = resource.wait_queue.popleft()
            resource.is_busy    = True
            resource.held_by    = next_pcb.pid
            next_pcb.waiting_for = None
            logger.resource_unblocked(time, next_pcb, resource_name)
            return next_pcb   # return it so simulation.py can move it back to READY

        return None