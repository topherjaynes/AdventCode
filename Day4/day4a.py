'''
"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:


..X...
.SAMX.
.A..A.
XMAS.S
.X....
The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:


'''


def wordsearch(file_path, word):
    #open the file and store in a grid. Assuming it's a uniform, but think through edgecases
    with open(file_path, 'r') as file:
        grid = [line.strip() for line in file.readlines()]

    #word directions. It can go any direction like a word search
    directions = [
        (0, 1),  # Right
        (0, -1), # Left
        (1, 0),  # Down
        (-1, 0), # Up
        (1, 1),  # Diagonal Down-Right
        (1, -1), # Diagonal Down-Left
        (-1, 1), # Diagonal Up-Right
        (-1, -1) # Diagonal Up-Left
    ]
    word_length = len(word)
    rows, cols = len(grid), len(grid[0])


    #seperated the function to check if word exisits in each directions
    #brute force first and then check to see if the letter we're on is the first of Word
    # if not then move on, no need to check directions
    def check_directions(x,y,dx,dy):
        for i in range(word_length):
            nx, ny = x + 1 * dx,y + i *dy
            if nx < 0 or nx >= rows or ny < 0 or ny >= cols or grid[nx][ny] != word[i]:
                return False
        return True

    #count occurences, is it a double for loop?
    count = 0
    for x in range(rows):
        for y in range(cols):
            #moving across all the cols first
            #check directions from coordinate
            for dx, dy in directions:
                if check_directions(x, y, dx,dy)
                    count +=1
    return count

result = wordsearch('/Users/topherjaynes/Desktop/AdventCode/Day4/input4.txt', 'XMAS')
print("Total occurrences of XMAS:", result)