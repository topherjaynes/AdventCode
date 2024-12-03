
'''
--- Day 2: Red-Nosed Reports ---
Fortunately, the first location The Historians want to search isn't a long walk from the Chief Historian's office.

While the Red-Nosed Reindeer nuclear fusion/fission plant appears to contain no sign of the Chief Historian, the engineers there run up to you as soon as they see you. Apparently, they still talk about the time Rudolph was saved through molecular synthesis from a single electron.

They're quick to add that - since you're already here - they'd really appreciate your help analyzing some unusual data from the Red-Nosed reactor. You turn to check if The Historians are waiting for you, but they seem to have already divided into groups that are currently searching every corner of the facility. You offer to help with the unusual data.

The unusual data (your puzzle input) consists of many reports, one report per line. Each report is a list of numbers called levels that are separated by spaces. For example:

7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
This example data contains six reports each containing five levels.

The engineers are trying to figure out which reports are safe. The Red-Nosed reactor safety systems can only tolerate levels that are either gradually increasing or gradually decreasing. So, a report only counts as safe if both of the following are true:

The levels are either all increasing or all decreasing.
Any two adjacent levels differ by at least one and at most three.
In the example above, the reports can be found safe or unsafe by checking those rules:

7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.
So, in this example, 2 reports are safe.

'''


def read_reports(filename):
    #list of list because it's not uniform
    data = []
    with open(filename, mode='r') as file:
        for line in file:
            # Split the line into integers and append to the data list
            report = list(map(int, line.split()))
            data.append(report)
    return data

def is_safe(report):
    differences = [
        report[i + 1] - report[i]
        for i in range(len(report) - 1)
    ]
    
    # Step 2: Check original rules
    if all(-3 <= diff <= 3 for diff in differences):
        increasing = all(diff > 0 for diff in differences)
        decreasing = all(diff < 0 for diff in differences)
        if increasing or decreasing:
            return True
    #step 3 check if removing a level helps
    for i in range(len(report)):
        modified_report = report[:i] + report[i + 1:]
        differences = [
            modified_report[j + 1] - modified_report[j]
            for j in range(len(modified_report) - 1)
        ]
        if all(-3 <= diff <= 3 for diff in differences):
            increasing = all(diff > 0 for diff in differences)
            decreasing = all(diff < 0 for diff in differences)
            if increasing or decreasing:
                return True

    return False

#Loop through our list of lists
def count_safe_reports(reports):
    return sum(1 for report in reports if is_safe(report))

reports = read_reports('/Users/topherjaynes/Desktop/AdventCode/Day2/input.txt')

print(count_safe_reports(reports))
