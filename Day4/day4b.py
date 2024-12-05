'''
--- Part Two ---
The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

M.S
.A.
M.S
Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?
'''


def wordsearch(file_path):
    with open(file_path, 'r') as file:
        grid = [line.strip() for line in file.readlines()]

    rows, cols = len(grid), len(grid[0])
    count = 0

    def check_diagonal(x1, y1, x2, y2, x3, y3):
        # Check both MAS and SAM on each diagonal
        chars = [grid[x1][y1], grid[x2][y2], grid[x3][y3]]
        return (chars == ['M', 'A', 'S']) or (chars == ['S', 'A', 'M'])

    def check_x_mas(x, y):
        # First, verify we have an 'A' at the center
        if grid[x][y] != 'A':
            return False

        # Check if all positions for the X pattern are within bounds
        if not (0 <= x-1 < rows and 0 <= x+1 < rows and
                0 <= y-1 < cols and 0 <= y+1 < cols):
            return False

        # Check forward diagonal (\)
        forward = check_diagonal(x-1, y-1, x, y, x+1, y+1)
        
        # Check backward diagonal (/)
        backward = check_diagonal(x-1, y+1, x, y, x+1, y-1)

        # Both diagonals must form valid patterns
        return forward and backward

    for x in range(rows):
        for y in range(cols):
            if check_x_mas(x, y):
                print(f"X-MAS found at center ({x},{y})")
                count += 1

    return count

result = wordsearch('/Users/topherjaynes/Desktop/AdventCode/Day4/input4b.txt')
#result = wordsearch('/Users/topherjaynes/Desktop/AdventCode/Day4/smallinputb.txt')
print("Total occurrences of X-MAS:", result)
