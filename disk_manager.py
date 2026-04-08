import os 
import csv
import math

class DiskManager:
    def __init__(self,disk_file="disk_sim.csv",  num_blocks=100, block_size=64):
        self.disk_file = disk_file
        self.num_blocks = num_blocks
        self.block_size = block_size
        self.initialize_disk()

    def initialize_disk(self):
        if not os.path.exists(self.disk_file):
            with open(self.disk_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["block_id", "data", "next_block"])
                for i in range(self.num_blocks):
                    writer.writerow([i, "." * self.block_size, -1])
            print(f"Initialized disk with {self.num_blocks} blocks of size {self.block_size} bytes each")
    #reads current state of the disk into memory
    def _get_all_rows(self):
        with open(self.disk_file, 'r') as f:
            return list(csv.reader(f))
    
    #saves the entire disk state back to CSV
    def _write_all_rows(self, rows):
        with open(self.disk_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
    #scans entire disk for blocks that aren't being used
    def find_free_blocks(self, needed):
        rows = self._get_all_rows()
        free_indices = []
        # Skip header at index 0
        for i in range(1, len(rows)):
            if rows[i][1] == "." * self.block_size:
                free_indices.append(i)
            if len(free_indices) == needed:
                return free_indices
        return []
    #simulates OS file writing 
    def write_file(self, pcb, filename, content):
        
        # Calculate how many blocks this content needs
        blocks_needed = math.ceil(len(content) / self.block_size)
        free_indices = self.find_free_blocks(blocks_needed)

        if not free_indices:
            return False, "Error: Disk Full"

        rows = self._get_all_rows()
        
        for i in range(blocks_needed):
            curr_idx = free_indices[i]
            # Slice the content for this specific block
            start = i * self.block_size
            chunk = content[start : start + self.block_size]
            # Pad the chunk if it's the last one and smaller than block_size
            chunk = chunk.ljust(self.block_size, '.')
            
            # Link to the next block in the list, or -1 if it's the last
            next_ptr = free_indices[i+1] - 1 if i < blocks_needed - 1 else -1
            
            rows[curr_idx][1] = chunk
            rows[curr_idx][2] = next_ptr

        self._write_all_rows(rows)
        pcb.add_file(filename) # Log the file to the PCB
        return True, f"Success: Wrote {filename} to {blocks_needed} blocks."
    def read_file(self, start_block_id):
        rows = self._get_all_rows()
        reconstructed_data = ""
        current_block_id = int(start_block_id)

        while current_block_id != -1:
             target_row = rows[current_block_id + 1]

             block_data = target_row[1]
             next_ptr = target_row[2]

             reconstructed_data += block_data.rstrip('.')
             current_block_id = next_ptr
        return reconstructed_data


    