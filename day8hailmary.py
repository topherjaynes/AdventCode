from collections import defaultdict
from itertools import combinations
import math

def parse_grid(input_text):
    """Parse the grid and return dictionary of frequencies to positions."""
    antennas = defaultdict(list)
    for y, line in enumerate(input_text.strip().split('\n')):
        for x, char in enumerate(line):
            if char != '.':
                antennas[char].append((x, y))
    return antennas

def is_collinear(p1, p2, p3, epsilon=1e-10):
    """
    Check if three points are collinear using the area method.
    Returns True if points form a line (area of triangle is approximately 0).
    """
    area = abs(p1[0]*(p2[1] - p3[1]) + p2[0]*(p3[1] - p1[1]) + p3[0]*(p1[1] - p2[1]))
    return area < epsilon

def is_point_between(p, a1, a2):
    """
    Check if point p lies on the line segment between a1 and a2.
    Used to optimize antinode search space.
    """
    # Check if point lies within the bounding box of the line segment
    min_x = min(a1[0], a2[0])
    max_x = max(a1[0], a2[0])
    min_y = min(a1[1], a2[1])
    max_y = max(a1[1], a2[1])
    
    return (min_x <= p[0] <= max_x and 
            min_y <= p[1] <= max_y)

def find_antinodes(grid, antenna1, antenna2):
    """Find all antinodes for a pair of antennas."""
    max_y = len(grid.split('\n'))
    max_x = len(grid.split('\n')[0])
    
    antinodes = set()
    
    # Add antenna positions themselves as potential antinodes
    antinodes.add(antenna1)
    antinodes.add(antenna2)
    
    # Calculate search bounds based on antenna positions
    min_x = max(0, min(antenna1[0], antenna2[0]) - 1)
    max_x = min(max_x, max(antenna1[0], antenna2[0]) + 2)
    min_y = max(0, min(antenna1[1], antenna2[1]) - 1)
    max_y = min(max_y, max(antenna1[1], antenna2[1]) + 2)
    
    # Check each potential point in bounded area
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            point = (x, y)
            if point != antenna1 and point != antenna2:  # Skip antenna positions here
                if is_collinear(point, antenna1, antenna2):
                    antinodes.add(point)
    
    return antinodes

def solve(input_text):
    """Find total number of unique antinode locations."""
    antennas = parse_grid(input_text)
    all_antinodes = set()
    
    # For each frequency with at least 2 antennas
    for freq, positions in antennas.items():
        if len(positions) < 2:
            continue
            
        # Check each pair of antennas
        for ant1, ant2 in combinations(positions, 2):
            antinodes = find_antinodes(input_text, ant1, ant2)
            all_antinodes.update(antinodes)
    
    return len(all_antinodes)

# Test with example input
test_input = """T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
.........."""

print(f"Test result: {solve(test_input)}")  # Should print 9

# Solve for actual input
with open('/Users/topherjaynes/Desktop/AdventCode/Day8/input.txt', 'r') as f:
    input_text = f.read()
print(f"Solution: {solve(input_text)}")