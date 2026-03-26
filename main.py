# main.py

import argparse
from logger import Logger
from memory_manager import MemoryManager
from resource_manager import ResourceManager
from scheduler import Scheduler
from simulation import run
from config import TOTAL_MEMORY, DEFAULT_QUANTUM, DEFAULT_POLICY, RESOURCES
from jobs import load_jobs

def main():
    # 1. read command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", default=DEFAULT_POLICY)
    parser.add_argument("--quantum", type=int, default=DEFAULT_QUANTUM)
    args = parser.parse_args()

    # 2. create your objects
    logger           = Logger()
    memory_manager   = MemoryManager(total_memory=TOTAL_MEMORY)
    resource_manager = ResourceManager()
    scheduler        = Scheduler(policy=args.policy, quantum=args.quantum)

    # 3. add shared resources from config
    for resource in RESOURCES:
        resource_manager.add_resource(resource)

    # 4. load jobs from jobs.py
    jobs = load_jobs()

    # 5. run the simulation
    run(scheduler, memory_manager, resource_manager, logger, jobs)

if __name__ == "__main__":
    main()