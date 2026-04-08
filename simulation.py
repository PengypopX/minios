from disk_manager import DiskManager
from memory_manager import MemoryManager
from scheduler import Scheduler
from pcb import State  


class Simulation:
    def __init__ (self, total_ram=1024):
        self.ready_queue = []
        self.blocked_queue = []
        self.finished_processes = []
        self.current_process = None

        # Initialize managers/hardware 
        self.disk = DiskManager("disk_sim.csv")
        self.memory = MemoryManager(total_ram)
        self.scheduler = Scheduler("FCFS")

        self.system_clock = 0

    def run(self, jobs, logger):
        while jobs or self.scheduler.ready_queue or self.blocked_queue or self.current_process:
            print(f"Time:{self.system_clock}")

            for job in jobs[:]: # 1. Arrival Logic; move from NEW to READY 
                if job.arrival_time <= self.system_clock:
                    if self.memory.allocate(job):   
                        self.scheduler.add_process(job)
                        jobs.remove(job)
                        print(f"[Memory] Allocated for Job {job.pid}")
                else:
                    free_space = self.memory.available_memory()
                    print(f"[Debug] Job {job.pid} needs {job.memory_required} memory. Available: {free_space}")
    
            if self.blocked_queue: # 2. Disk Logic, service blocked queue
                io_target = self.scheduler._io_sjf(self.blocked_queue)
                if io_target:
                    test_content = f"Data for job {io_target.pid} at time {self.system_clock}" * 5
                    success, message = self.disk.write_file(io_target, f"file_{io_target.pid}.txt", test_content)
                    io_target.state = State.READY
                    self.scheduler.add_process(io_target)
                    print (f"[Disk] {message}. Job {io_target.pid} moved to READY")

            if not self.current_process and self.scheduler.ready_queue: # 3. CPU Logic, select next process to run
                self.current_process = self.scheduler.select_next()
                if self.current_process:
                    self.current_process.state = State.RUNNING
                    logger.process_selected(self.system_clock, self.current_process)
                    if self.current_process.start_time is None:
                        self.current_process.start_time = self.system_clock

            if self.current_process: # 4. CPU Logic, tick current process
                result = self.scheduler.tick(self.current_process, logger,  self.system_clock)
                if result == "preempted":
                    self.current_process =  None
                    print(f"[Kernel] Quantum Expired. Process Preempted")
                elif result == "terminated":
                    self.finished_processes.append(self.current_process)
                    self.memory.release(self.current_process)
                    self.current_process = None
                elif self.current_process and self.system_clock % 5 == 0:
                    self.current_process.request_io(32)
                    self.blocked_queue.append(self.current_process)
                    print(f"[Process {self.current_process.pid}] Requested I/O, moved to BLOCKED")
                    self.current_process = None

            self.system_clock += 1