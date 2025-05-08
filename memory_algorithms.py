# Fragmentation Calculation
def calculate_fragmentation(memory_blocks):
    free_space = sum(block.size for block in memory_blocks if not block.occupied)
    total_space = sum(block.size for block in memory_blocks)
    return free_space / total_space * 100 if total_space > 0 else 0

# Memory Block Class
class MemoryBlock:
    def __init__(self, size, start_address):
        self.size = size
        self.start_address = start_address
        self.occupied = False
        self.process_id = None

    def __repr__(self):
        return f"<Block {self.size} @ {self.start_address} - {'Used' if self.occupied else 'Free'}>"

# Memory Allocation Function
def allocate(memory_blocks, block, process_id, process_size):
    if block.size > process_size:  # Split block if the size is greater than the process size
        remaining_size = block.size - process_size
        new_block = MemoryBlock(remaining_size, block.start_address + process_size)
        block.size = process_size
        memory_blocks.insert(memory_blocks.index(block) + 1, new_block)
    
    # Mark the block as occupied
    block.occupied = True
    block.process_id = process_id

# Allocation Strategies: First Fit, Best Fit, Worst Fit
def first_fit(memory_blocks, process_id, process_size):
    for block in memory_blocks:
        if not block.occupied and block.size >= process_size:
            allocate(memory_blocks, block, process_id, process_size)
            return True
    return False

def best_fit(memory_blocks, process_id, process_size):
    suitable_blocks = [b for b in memory_blocks if not b.occupied and b.size >= process_size]
    if not suitable_blocks:
        return False
    best = min(suitable_blocks, key=lambda b: b.size)
    allocate(memory_blocks, best, process_id, process_size)
    return True

def worst_fit(memory_blocks, process_id, process_size):
    suitable_blocks = [b for b in memory_blocks if not b.occupied and b.size >= process_size]
    if not suitable_blocks:
        return False
    worst = max(suitable_blocks, key=lambda b: b.size)
    allocate(memory_blocks, worst, process_id, process_size)
    return True
