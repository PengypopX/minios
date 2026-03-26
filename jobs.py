from pcb import PCB
def load_jobs():
    jobs = [
        PCB(pid=1, arrival_time=0, burst_time=5, memory_required=128),
        PCB(pid=2, arrival_time=1, burst_time=25, memory_required=256),
        PCB(pid=3, arrival_time=2, burst_time=15, memory_required=128),
        PCB(pid=4, arrival_time=3, burst_time=8, memory_required=100),
        PCB(pid=5, arrival_time=4, burst_time=20, memory_required=512)
    ]
    return jobs
