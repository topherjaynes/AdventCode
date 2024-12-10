def load_input(file_path):
    equations = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            target_value =  int(parts[0])
            numbers = [int(x) for x in parts[1].split()]
            equations.append((target_value, numbers))
    
    return equations

def evaluate_equation(numbers, operators):
    result = numbers[0]
    for i in range(1, len(numbers)):
        if operators[i - 1] == '+':
            result += numbers[i]
        elif operators[i - 1] == '*':
            result *= numbers[i]
        elif operators[i - 1] == '||':
            result = int(str(result) + str(numbers[i])) 
    return result

def find_valid_equations(numbers, target_value):
    valid_combinations = []
    def backtrack(index, current_operators):
        if index == len(numbers) - 1:
            if evaluate_equation(numbers, current_operators) == target_value:
                valid_combinations.append(current_operators.copy())
            return

        for operator in ('+', '*', '||'):
            current_operators.append(operator)
            backtrack(index + 1, current_operators)
            current_operators.pop()

    backtrack(0, [])
    return valid_combinations

def calculate_total_calibration_result(equations):
    total_result = 0
    for target_value, numbers in equations:
        if find_valid_equations(numbers, target_value):
            total_result += target_value
    return total_result


def main():
    eqs = load_input('/Users/topherjaynes/Desktop/AdventCode/day7/input7.txt')
    total_calibration_result = calculate_total_calibration_result(eqs)
    print(f"Total calibration result: {total_calibration_result}")

if __name__ == "__main__":
    main()