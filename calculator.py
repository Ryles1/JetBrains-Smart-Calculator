from collections import deque


class Calculator:
    precedence = {'*': 2, '/': 2, '+': 1, '-': 1}

    def __init__(self):
        self. vars = {}

    def addition(self, nums):
        total = 0
        for i, num in enumerate(nums):
            value = 0
            if '-' in num or '+' in num:
                pass
            elif num in self.vars.keys():
                value = int(self.vars[num])
            else:
                value = int(num)
            if i == 0:
                total += value
            elif '-' in num or '+' in num:
                continue
            else:
                if self.is_negative(nums[i-1]):
                    total += (value*-1)
                else:
                    total += value
        return total

    def is_negative(self, symbols):
        if symbols.count('-') % 2 == 0:
            return False
        return True

    def var_assign(self, s):
        var = s.split('=')[0].strip()
        value = s.split('=')[1].strip()
        if value in self.vars.keys():
            value = self.vars[value]
        if self.var_ok(var) and self.value_ok(value):
            self.vars[var] = value
        else:
            print('Invalid identifier')

    def var_ok(self, check_var):
        if not check_var.isalpha():
            return False
        return True

    def value_ok(self, check_value):
        if not check_value.isdigit():
            return False
        return True

    def postfix(self, expression):
        # convert expression to postfix notation using deque as a queue
        # requires string to have spaces between operands and operators
        postfix_result = []
        operators = deque()
        temp_pop = None
        for index, item in enumerate(expression):
            # numbers go in the queue
            if item.isnumeric():
                postfix_result.append(item)
            # if item is a stored variable, add its value to the queue
            elif item in self.vars.keys():
                postfix_result.append(self.vars[item])
            # if stack empty or item is (, add to the queue
            elif len(operators) == 0 or operators[-1] == '(':
                operators.append(item)
            # if item is higher precedence operator than top of stack, put on stack
            elif item == '(':
                operators.append(item)
            elif item == ')':
                temp_pop = operators.pop()
                while temp_pop != '(':
                    postfix_result.append(temp_pop)
                    temp_pop = operators.pop()
            elif self.precedence[item] > self.precedence[operators[-1]]:
                operators.append(item)
            elif self.precedence[item] <= self.precedence[operators[-1]]:
                temp_pop = operators.pop()
                while self.precedence[temp_pop] < self.precedence[item] or temp_pop == '(':
                    postfix_result.append(temp_pop)
                    temp_pop = operators.pop()
                operators.append(item)
                postfix_result.append(temp_pop)
            else:
                pass
        if len(operators) != 0:
            while len(operators) > 0:
                postfix_result.append(operators.pop())
        return postfix_result

    def evaluate(self, a, b, operator):
        if operator == '*':
            return a*b
        elif operator == '/':
            return a/b
        elif operator == '+':
            return a+b
        elif operator == '-':
            return a-b
        else:
            return None

    def calculate(self, expr):
        postfix = self.postfix(expr)
        result = deque()
        for i in postfix:
            if i.isnumeric():
                result.append(int(i))
            else:
                temp2 = int(result.pop())
                temp1 = int(result.pop())
                result.append(self.evaluate(temp1, temp2, i))
        answer = result[0]
        return answer


def commands(input):
    if input == '/help':
        print('The program calculates the sum of numbers')
        return False
    elif input == '/exit':
        return True
    else:
        print('Unknown command')
        return False


def bad_input(inp):
    for i, c in enumerate(inp):
        if c == '*':
            if inp[i+1] == '*':
                return True
        elif c == '/':
            if inp[i + 1] == '/':
                return True
    if inp.count('(') != inp.count(')'):
        return True
    return False


def parse_input(inp_string):
    neg_start = False
    temp = []
    parsed_string = inp_string.replace(' ', '')
    parse_list = []
    for i, c in enumerate(parsed_string):
        # group all common characters (alphas for variables, numerics for numbers, operators)
        if i == 0 and c == '-':
            neg_start = True
        elif i+1 == len(parsed_string):
            if temp != [] and c.isnumeric():
                temp.append(c)
                parse_list.append(''.join(temp))
                temp.clear()
            else:
                if temp != []:
                    parse_list.append(''.join(temp))
                temp.clear()
                parse_list.append(c)
        elif c == '*' or c == '/' or c == '(' or c == ')':
            parse_list.append(c)
        elif c.isnumeric() and (parsed_string[i+1].isnumeric()):
            temp.append(c)
        elif c.isnumeric() and not parsed_string[i+1].isnumeric():
            temp.append(c)
            parse_list.append(''.join(temp))
            temp.clear()
        elif c.isalpha() and (parsed_string[i+1].isalpha()):
            temp.append(c)
        elif c.isalpha() and not parsed_string[i+1].isalpha():
            temp.append(c)
            parse_list.append(''.join(temp))
            temp.clear()
        elif c=='-' and (parsed_string[i + 1] == '-'):
            temp.append(c)
        elif c=='-' and not (parsed_string[i + 1] == '-'):
            temp.append(c)
            parse_list.append(''.join(temp))
            temp.clear()
        elif c=='+' and (parsed_string[i + 1] == '+'):
            temp.append(c)
        elif c=='+' and not (parsed_string[i + 1] == '+'):
            temp.append(c)
            parse_list.append(''.join(temp))
            temp.clear()
        else:
            pass
    # if first character was negative, change first int to negative
    if neg_start:
        parse_list[0] *= -1
    # replace groups of - and + with single characters
    for i, c in enumerate(parse_list):
        if '+' in c:
            parse_list[i] = '+'
        elif '-' in c:
            if c.count('-') % 2 == 0:
                parse_list[i] = '+'
            else:
                parse_list[i] = '-'
    #parsed_string = ' '.join(parse_list)
    return parse_list


if __name__ == '__main__':
    exit = False
    calc = Calculator()
    while exit is False:
        user_input = input().strip()
        if user_input.startswith('/'):
            exit = commands(user_input)
        elif user_input == '':
            continue
        elif '=' in user_input:
            calc.var_assign(user_input)
        elif user_input.isalpha():
            if user_input in calc.vars.keys():
                print(calc.vars[user_input])
            else:
                print('Unknown variable')
        elif user_input.isnumeric():
            print(user_input)
        elif bad_input(user_input):
            print('Invalid expression')
            continue
        else:
            calc_list = parse_input(user_input)
            print(calc.calculate(calc_list))
    print('Bye!')