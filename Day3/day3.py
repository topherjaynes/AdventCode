'''
"Our computers are having issues, so I have no idea if we have any Chief Historians in stock! You're welcome to check the warehouse, though," says the mildly flustered shopkeeper at the North Pole Toboggan Rental Shop. The Historians head out to take a look.

The shopkeeper turns to you. "Any chance you can see why our computers are having issues again?"

The computer appears to be trying to run a program, but its memory (your puzzle input) is corrupted. All of the instructions have been jumbled up!

It seems like the goal of the program is just to multiply some numbers. It does that with instructions like mul(X,Y), where X and Y are each 1-3 digit numbers. For instance, mul(44,46) multiplies 44 by 46 to get a result of 2024. Similarly, mul(123,4) would multiply 123 by 4.

However, because the program's memory has been corrupted, there are also many invalid characters that should be ignored, even if they look like part of a mul instruction. Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.

For example, consider the following section of corrupted memory:

xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
Only the four highlighted sections are real mul instructions. Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

Scan the corrupted memory for uncorrupted mul instructions. What do you get if you add up all of the results of the multiplications?
--- Part Two ---
As you scan through the corrupted memory, you notice that some of the conditional statements are also still intact. If you handle some of the uncorrupted conditional statements in the program, you might be able to get an even more accurate result.

There are two new instructions you'll need to handle:

The do() instruction enables future mul instructions.
The don't() instruction disables future mul instructions.
Only the most recent do() or don't() instruction applies. At the beginning of the program, mul instructions are enabled.

For example:

xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
This corrupted memory is similar to the example from before, but this time the mul(5,5) and mul(11,8) instructions are disabled because there is a don't() instruction before them. The other mul instructions function normally, including the one at the end that gets re-enabled by a do() instruction.

This time, the sum of the results is 48 (2*4 + 8*5).

Handle the new instructions; what do you get if you add up all of the results of just the enabled multiplications?
'''
import re

def parse_and_sum(file_path):
    # Step 1: Read the file content
    with open(file_path, 'r') as file:
        content = file.read()

    
    # Step 2: Find all valid `mul(X,Y)` instructions
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, content)
    print(matches)
    # Step 3: Evaluate and sum the results
    total_sum = 0
    for match in matches:
        x, y = map(int, match)  # Convert matched strings to integers
        #print(x*y)
        total_sum += x * y
        print(total_sum)
    
    return total_sum

def read_reports(filename):
    #list of list because it's not uniform
    data = []
    with open(filename, mode='r') as file:
        for line in file:
            # Split the line into integers and append to the data list
            #report = list(map(int, line.split()))
            data.append(line)
    return data

#Okay this is the second method

def parse_and_sum_with_conditions(file_path):
    # Step 1: Read the file content
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Step 2: Define patterns for `do()`, `don't()`, and `mul(X,Y)`
    pattern = r"(do\(\)|don't\(\)|mul\((\d{1,3}),(\d{1,3})\))"
    matches = re.findall(pattern, content)
    
    # Step 3: Process matches and track state
    enabled = True
    total_sum = 0

    for match in matches:
        instruction, x, y = match
        
        if instruction == "do()":
            enabled = True
        elif instruction == "don't()":
            enabled = False
        elif "mul(" in instruction and enabled:
            # Evaluate the `mul(X,Y)` instruction if enabled
            x, y = int(x), int(y)
            total_sum += x * y

    return total_sum

#part2
result2 = parse_and_sum_with_conditions('/Users/topherjaynes/Desktop/AdventCode/Day3/input1.txt')
print(result2)

#part 1
#result = parse_and_sum('/Users/topherjaynes/Desktop/AdventCode/Day3/input1.txt')
#print(result)

#testing the file
#print(read_reports('/Users/topherjaynes/Desktop/AdventCode/Day3/input1.txt'))

#is there a way without regex?
def parse_and_sum_without_regex(file_path):
    # Step 1: Read the file content
    with open(file_path, 'r') as file:
        content = file.read()

    # Step 2: Initialize variables
    enabled = True
    total_sum = 0
    i = 0

    # Step 3: Process the string character by character
    while i < len(content):
        if content[i:i+4] == "do()":
            enabled = True
            i += 4  # Skip past "do()"
        elif content[i:i+7] == "don't()":
            enabled = False
            i += 7  # Skip past "don't()"
        elif content[i:i+4] == "mul(":
            if enabled:
                # Find the closing parenthesis
                end_index = content.find(")", i)
                if end_index != -1:
                    # Extract the arguments inside "mul(...)"
                    arguments = content[i+4:end_index]
                    if "," in arguments:
                        parts = arguments.split(",")
                        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                            x, y = map(int, parts)
                            total_sum += x * y
                    i = end_index + 1  # Skip past the closing parenthesis
                else:
                    i += 4  # Skip "mul(" if no closing parenthesis found
            else:
                # Skip past this mul if disabled
                i += 4
        else:
            # Move to the next character
            i += 1

    return total_sum

#trying part two without regex
result = parse_and_sum_without_regex('/Users/topherjaynes/Desktop/AdventCode/Day3/input1.txt')
print("Total Sum with Conditions (No Regex):", result)
