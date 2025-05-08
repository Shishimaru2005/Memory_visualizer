from memory_algorithms import MemoryBlock

def generate_memory_blocks(total_size, block_sizes):
    memory_blocks = []
    start = 0
    for size in block_sizes:
        memory_blocks.append(MemoryBlock(size, start))
        start += size
    return memory_blocks