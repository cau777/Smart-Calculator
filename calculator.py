import string

from collections import deque


def main():
    print('/help for info')
    while True:
        s = read_input()

        if s.count('=') > 1:
            print('Invalid Assignment')
            continue

        if s.count('|') > 0:
            print('Invalid Assignment')
            continue

        if is_expression(s):
            # Expression
            result = solve_expression(s)
            if result is not None:
                print(result)
        else:
            # Variable
            global assignment
            assignment = True

            content = s.split('=')
            variable_name = content[0].strip()

            if valid_name(variable_name):
                expression = content[1].strip()
                result = solve_expression(expression)
                if result is not None:
                    variables[variable_name] = result
            else:
                print('Invalid identifier')


def print_invalid():
    global assignment
    if assignment:
        print('Invalid Assignment')
    else:
        print('Invalid Operation')


def convert_to_postfix(parts: list[str]):
    result = deque()
    operator_stack = deque()
    parenthesis_layer = 0

    for p in parts:
        if p.startswith('('):
            parenthesis_layer += 1
            p = p.lstrip('(')

        if p.endswith(')'):
            parenthesis_layer -= 1
            p = p.rstrip(')')

        # Variable
        if p.isalpha():
            if p in variables.keys():
                result.append(variables[p])
                continue
            else:
                print('Unknown Variable')
                return None

        try:
            # Number
            value = int(p)
            result.append(value)
        except ValueError:
            # Operator
            op = get_operator(p)
            if op is not None:
                priority = get_priority(op, parenthesis_layer)

                if len(operator_stack) == 0:
                    operator_stack.append((op, priority))
                    continue

                first_operator = operator_stack.pop()

                if first_operator[1] < priority:
                    operator_stack.append(first_operator)
                    operator_stack.append((op, priority))
                    continue

                while first_operator[1] >= priority:
                    result.append(first_operator[0])

                    if len(operator_stack) == 0:
                        break
                    else:
                        first_operator = operator_stack.pop()
                operator_stack.append((op, priority))
            else:
                # Unknown
                print_invalid()
                return None

    for _n in range(len(operator_stack)):
        result.append(operator_stack.pop()[0])

    if parenthesis_layer != 0:
        print_invalid()
        return None

    return result


def solve_expression(expression: str):
    parts = split_parts(expression)

    if parts is None:
        return None

    postfix = convert_to_postfix(parts)

    if postfix is None:
        return None

    hold_stack = deque()

    for _n in range(len(postfix)):
        element = postfix.popleft()

        if type(element) == int:
            # Number
            hold_stack.append(element)
        else:
            # Operator
            hold_stack.append(solve_operation(hold_stack.pop(), hold_stack.pop(), element))

    return int(hold_stack.pop())


def solve_operation(n1: int, n2: int, operator: str):
    if operator == '+':
        return n2 + n1
    elif operator == '-':
        return n2 - n1
    elif operator == '*':
        return n2 * n1
    elif operator == '/':
        return n2 / n1
    else:
        return n2 ** n1


def split_parts(expression: str):
    divisions = []
    expression = expression.replace(' ', '')

    for letter_num in range(len(expression)):
        letter = expression[letter_num]

        if is_operator(letter):
            if letter_num == len(expression):
                print_invalid()
                return None

            unary_minus = is_unary_minus(expression, letter_num)

            if letter_num != 0 and not is_operator(expression[letter_num - 1]) or unary_minus:
                divisions.append('|')

            divisions.append(letter)

            if letter_num != len(expression) - 1 and not is_operator(expression[letter_num + 1]) and \
                    not unary_minus:
                divisions.append('|')
        else:
            divisions.append(letter)

    parts = "".join(divisions).split('|')
    return parts


def is_unary_minus(expression: str, index: int):
    if 0 < index < len(expression) - 1:  # If in limits
        return is_operator(expression[index - 1]) and expression[index] == '-' and not is_operator(
            expression[index + 1])
    return False


def is_operator(target: str):
    return get_operator(target) is not None


def get_operator(target: str):
    if target == '*' or target == '/' or target == '^':
        return target
    elif target == ('+' * len(target)):
        return '+'
    elif target == ('-' * len(target)):
        return '+' if len(target) % 2 == 0 else '-'
    else:
        return None


def get_priority(operator: str, layer: int):
    return operators[operator] + layer * 10


def is_expression(exp: str):
    return '=' not in exp


def valid_name(name: str):
    for letter in name:
        if letter not in string.ascii_letters:
            return False
    return True


def read_input():
    while True:
        s = input()

        if s.startswith('/'):
            if s == '/exit':
                print('Bye!')
                exit()
            elif s == '/help':
                print('The program supports operators (+, -, *, /, ^).\n'
                      'You can write expressions with numbers, operators, variables and parenthesis'
                      'in the format: "-b + 4 - (5 + 6) * 9" '
                      'or "-2+myvariable*-8+14*(15-17)--1"\n'
                      'To assign variable, use "=": "a = 2 + 8"\n'
                      'To get the value of a variable, simply write its identifier')
                print('Available Commands:\n'
                      '/help for more info\n'
                      '/exit to exit the program')
            else:
                print('Unknown command')
            continue

        if len(s) == 0:
            continue

        return s


operators = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
variables = {}
assignment = False
main()
