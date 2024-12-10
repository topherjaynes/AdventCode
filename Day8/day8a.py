from collections import defaultdict
from itertools import combinations
import math

def parse_grid(input_text):
    """Parse the grid and return dictionary of frequencies to positions."""
    antennas = defaultdict(list)
    lines = input_text.strip().split('\n')
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != '.':
                antennas[char].append((x, y))
    return antennas, len(lines), len(lines[0])

def is_collinear(p1, p2, p3, epsilon=1e-10):
    """
    Check if three points are collinear using the area method.
    Returns True if points form a line (area of triangle is approximately 0).
    """
    area = abs(p1[0]*(p2[1] - p3[1]) + p2[0]*(p3[1] - p1[1]) + p3[0]*(p1[1] - p2[1]))
    return area < epsilon

def find_antinodes(antenna1, antenna2, max_x, max_y):
    """
    Find all antinodes for a pair of antennas by checking every grid position.
    Now checks the entire grid as antinodes can appear beyond antenna positions.
    """
    antinodes = set()
    
    # Add antenna positions themselves as antinodes
    antinodes.add(antenna1)
    antinodes.add(antenna2)
    
    # Check every point in the grid
    for y in range(max_y):
        for x in range(max_x):
            point = (x, y)
            if point != antenna1 and point != antenna2:
                if is_collinear(point, antenna1, antenna2):
                    antinodes.add(point)
    
    return antinodes

def solve(input_text):
    """Find total number of unique antinode locations."""
    antennas, max_y, max_x = parse_grid(input_text)
    all_antinodes = set()
    
    # For each frequency with at least 2 antennas
    for freq, positions in antennas.items():
        if len(positions) < 2:
            continue
        
        # Check each pair of antennas of the same frequency
        for ant1, ant2 in combinations(positions, 2):
            antinodes = find_antinodes(ant1, ant2, max_x, max_y)
            all_antinodes.update(antinodes)
    
    return len(all_antinodes)

# Test with example input
test_input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

print(f"Test result: {solve(test_input)}")  # Should print 34

# Solve for actual input
with open('/Users/topherjaynes/Desktop/AdventCode/Day8/input.txt', 'r') as f:
    input_text = f.read()
print(f"Solution: {solve(input_text)}")