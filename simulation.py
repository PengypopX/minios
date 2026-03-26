# simulation.py

from pcb import State

def run(scheduler, memory_manager, resource_manager, logger, jobs):
    current_time    = 0
    current_process = None
    remaining_jobs  = list(jobs)   # copy of jobs not yet arrived

    # simulation runs until all jobs are terminated
    while remaining_jobs or scheduler.ready_queue or current_process:

        # 1. check if any jobs arrive at this time
        for job in list(remaining_jobs):
            if job.arrival_time == current_time:
                remaining_jobs.remove(job)
                success = memory_manager.allocate(job)
                if success:
                    logger.memory_allocated(current_time, job)
                    scheduler.add_process(job)
                    logger.process_arrived(current_time, job)
                else:
                    logger.memory_denied(current_time, job)
                    job.state = State.BLOCKED

        # 2. select next process if CPU is idle
        if current_process is None:
            current_process = scheduler.select_next()
            if current_process:
                current_process.state = State.RUNNING
                if current_process.start_time is None:
                    current_process.start_time = current_time
                logger.process_selected(current_time, current_process)

        # 3. tick the current process
        if current_process:
            result = scheduler.tick(current_process, logger, current_time)

            if result == "terminated":
                memory_manager.release(current_process)
                logger.memory_released(current_time, current_process)
                # check if it was holding a resource
                if current_process.waiting_for:
                    next_pcb = resource_manager.release(
                        current_process, current_process.waiting_for, logger, current_time
                    )
                    if next_pcb:
                        scheduler.add_process(next_pcb)
                current_process = None

            elif result == "preempted":
                current_process = None

        # 4. advance time
        current_time += 1