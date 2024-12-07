def load_map(file_path):
    with open(file_path, 'r') as file:
        grid = [list(line.strip()) for line in file]
    # Debug: Print the grid
    
    # Find starting position and direction
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == '^':
                return grid, (x, y, 'up')  # (x, y, direction)
    return grid, None

def detect_loop(path):
    """
    Detect if there's a loop by looking for repeated positions with the same direction.
    """
    seen = {}  # (x, y, direction) -> first occurrence
    for i, (x, y, direction) in enumerate(path):
        pos = (x, y, direction)  # Include direction
        if pos in seen:
            return True
        seen[pos] = i
    return False

def find_loop_positions(grid, original_path, start_pos):
    start_x, start_y, _ = start_pos
    valid_positions = []
    
    # Only check positions in the original path
    path_positions = {(x, y) for x, y, _ in original_path}
    
    for x, y in path_positions:
        # Skip start position
        if x == start_x and y == start_y:
            continue
        
        # Try placing obstruction
        test_grid = [row[:] for row in grid]
        test_grid[y][x] = '#'
        
        _, path = simulate_path_with_tracking(test_grid, start_pos)
        
        # Check if this creates a loop
        visited_states = set()
        for px, py, facing in path:
            state = (px, py, facing)
            if state in visited_states:
                valid_positions.append((x, y))
                break
            visited_states.add(state)
    
    return valid_positions

def simulate_path_with_tracking(grid, start_pos):
    """
    Modified version of simulate_path that returns both the count and the path,
    with early stopping if a loop is detected.
    """
    visited = set()
    path = []
    current = start_pos
    seen = {}  # For loop detection

    while True:
        x, y, facing = current
        if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
            visited.add((x, y))
            path.append((x, y, facing))

            # Loop detection
            state = (x, y, facing)
            if state in seen:
                return len(visited), path  # Early stopping
            seen[state] = True

        next_pos = move_guard(grid, current)
        nx, ny, _ = next_pos

        # Stop if we've left the map
        if (ny < 0 or ny >= len(grid) or 
            nx < 0 or nx >= len(grid[0])):
              break

        current = next_pos

    return len(visited), path


def move_guard(grid, pos):
    # Direction mappings: current -> (dx, dy, new_direction)
    directions = {
        'up': (0, -1, 'up'),
        'right': (1, 0, 'right'),
        'down': (0, 1, 'down'),
        'left': (-1, 0, 'left')
    }
    
    # Right turn mappings
    turns = {
        'up': 'right',
        'right': 'down',
        'down': 'left',
        'left': 'up'
    }
    
    x, y, facing = pos
   # print(pos)
    dx, dy, _ = directions[facing]
    next_x, next_y = x + dx, y + dy
    
    # Check if next position is blocked or out of bounds
    if (0 <= next_y < len(grid) and 
        0 <= next_x < len(grid[0]) and 
        grid[next_y][next_x] == '#'):
        # Turn right
        return (x, y, turns[facing])
    
    # Move forward
    return (next_x, next_y, facing)

def simulate_path(grid, start_pos):
    visited = set()
    current = start_pos
    
    while True:
        x, y, _ = current
        # Add current position to visited set
        if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
            visited.add((x, y))
        
        next_pos = move_guard(grid, current)
        nx, ny, _ = next_pos
        
        # Check if guard has left the map
        nx, ny, _ = next_pos
        if (ny < 0 or ny >= len(grid) or 
            nx < 0 or nx >= len(grid[0])):
            break
            
        current = next_pos
    
    return len(visited)

def find_possible_obstructions(grid, start_pos):
    start_x, start_y, _ = start_pos
    valid_positions = []

    # Try each empty position
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            # Skip if not empty or is start position
            if grid[y][x] != '.' or (x == start_x and y == start_y):
                continue

            # Create a copy of the grid with new obstruction
            test_grid = [row[:] for row in grid]
            test_grid[y][x] = '#'

            # Run simulation and check for loops (using modified detect_loop)
            _, path = simulate_path_with_tracking(test_grid, start_pos) 
            if detect_loop(path):  # You might not need detect_loop anymore
                valid_positions.append((x, y))
                print(f"Found valid obstruction at ({x}, {y})")

    return valid_positions

'''def main():
    grid, start_pos = load_map('/Users/topherjaynes/Desktop/AdventCode/day6/day6.txt')
    print(start_pos)
    if start_pos:
        result = simulate_path(grid, start_pos)
        print(f"The guard visits {result} distinct positions")'''
def main():
    grid, start_pos = load_map('/Users/topherjaynes/Desktop/AdventCode/day6/day6.txt')
    if start_pos:
        # Part 1: Get original path
        count, original_path = simulate_path_with_tracking(grid, start_pos)
        print(f"Part 1: Guard visits {count} positions")
        
        # Part 2: Find positions that create loops
        valid_positions = find_loop_positions(grid, original_path, start_pos)
        print(f"Part 2: Found {len(valid_positions)} positions that create loops")
        
        # Visualize one solution if any found
        if valid_positions:
            x, y = valid_positions[0]
            test_grid = [row[:] for row in grid]
            test_grid[y][x] = 'O'
            print("\nExample solution:")
            for row in test_grid:
                print(''.join(row))


if __name__ == "__main__":
    main()