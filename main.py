# main.py
import os
import argparse
from logger import Logger
from memory_manager import MemoryManager
from resource_manager import ResourceManager
from scheduler import Scheduler
from simulation import Simulation
from config import TOTAL_MEMORY, DEFAULT_QUANTUM, DEFAULT_POLICY, RESOURCES
from jobs import load_jobs


def main():
    if os.path.exists("disk_sim.csv"):
        os.remove("disk_sim.csv")
    # 1. read command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", default=DEFAULT_POLICY)
    parser.add_argument("--quantum", type=int, default=DEFAULT_QUANTUM)
    args = parser.parse_args()

    # 2. create your objects
    logger = Logger()
    sim = Simulation(TOTAL_MEMORY)

    # 4. load jobs from jobs.py
    jobs = load_jobs()

    # 5. run the simulation
    sim.run(jobs, logger)
    logger.print_summary()


if __name__ == "__main__":
    main()
