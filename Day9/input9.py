def read_input(file_path):
    with open(file_path, 'r') as f:
        return f.read().strip()
    
def parse_disk_map(disk_map):
    """
    Convert disk map string to file sizes and gap sizes
    ex 12345 -> [1,3,5] gaps [2,4]
    """
    file_sizes = [int(disk_map[i]) for i in range(0, len(disk_map),2)]
    gap_sizes  = [int(disk_map[i]) for i in range(1, len(disk_map),2)]
    return file_sizes, gap_sizes

def create_block_representation(file_sizes, gap_sizes):
    """
    Convert sizes into a block representation.
    Example: files [1,3,5], gaps [2,4] -> "0..111....22222"
    """
    blocks = []
    current_file_id = 0
    
    # Interleave files and gaps
    for file_size, gap_size in zip(file_sizes, gap_sizes + [0]):  # Add 0 for last file
        # Add file blocks
        blocks.extend([str(current_file_id)] * file_size)
        # Add gap blocks
        blocks.extend(['.'] * gap_size)
        current_file_id += 1
    
    return ''.join(blocks)

def find_leftmost_gap(blocks):
    """Find the position of the leftmost '.' character."""
    return blocks.index('.') if '.' in blocks else None

def find_rightmost_file(blocks):
    """Find the rightmost file block and its starting position."""
    # Convert to list for easier manipulation
    blocks_list = list(blocks)
    # Work backwards to find first non-'.' character
    for i in range(len(blocks_list) - 1, -1, -1):
        if blocks_list[i] != '.':
            # Find start of this file block
            file_id = blocks_list[i]
            while i >= 0 and blocks_list[i] == file_id:
                i -= 1
            return file_id, i + 1
    return None, None

def move_block(blocks, from_pos, to_pos):
    """Move a single block from one position to another."""
    blocks_list = list(blocks)
    file_id = blocks_list[from_pos]
    blocks_list[from_pos] = '.'
    blocks_list[to_pos] = file_id
    return ''.join(blocks_list)

def compact_disk(blocks):
    """
    Compact the disk by moving files one block at a time.
    Returns list of states for visualization.
    """
    states = [blocks]
    while '.' in blocks:
        # Find moves
        gap_pos = find_leftmost_gap(blocks)
        file_id, file_start = find_rightmost_file(blocks)
        
        if gap_pos is None or file_id is None:
            break
            
        # Move one block
        blocks = move_block(blocks, file_start, gap_pos)
        states.append(blocks)
    
    return states

def calculate_checksum(final_state):
    """
    Calculate checksum by multiplying position by file ID for each block.
    """
    checksum = 0
    for pos, char in enumerate(final_state):
        if char != '.':
            checksum += pos * int(char)
    return checksum

def main():
    # Read input
    disk_map = read_input('/Users/topherjaynes/Desktop/AdventCode/Day9/day9a.txt')
    #print(f"Input disk map: {disk_map}")
    
    # Parse into sizes
    file_sizes, gap_sizes = parse_disk_map(disk_map)
    
    # Create initial block representation
    initial_blocks = create_block_representation(file_sizes, gap_sizes)
    #print(f"Initial state:")
    #print(initial_blocks)
    
    # Compact disk
    states = compact_disk(initial_blocks)
    #print("\nFinal state:")
    #print(states[-1])
    
    # Calculate checksum
    checksum = calculate_checksum(states[-1])
    print(f"\nChecksum: {checksum}")


if __name__ == "__main__":
    main()