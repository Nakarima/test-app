import multiprocessing as mp

operators = '+-/*'

def calc(expression):
    try:
        res = expr_evaluation(postfix_transform(expression))
        return res
    except Exception as e:
        raise Exception(str(e))

def postfix_evaluation(expression):
    if len(expression) == 1:
        return expression[0]

    stack = []
    operators = {'+': lambda x, y: x + y,
                 '-': lambda x, y: x - y,
                 '*': lambda x, y: x * y,
                 '/': lambda x, y: x / y}
    for symbol in expression:
        if is_digit(symbol):
            stack.append(symbol)
        else:
            s2 = float(stack.pop())
            s1 = float(stack.pop())
            stack.append(float(operators[symbol](s1,s2)))
    result = round(stack[0], 4)
    if result.is_integer():
        return int(result)
    return result

def expr_evaluation(expression):
    if len(expression) < 7:
        return postfix_evaluation(expression)

    last_operator = expression.pop()
    operands_count = 0
    operators_count = 1
    index = len(expression) - 1

    while operators_count != operands_count:
        if expression[index] in operators:
            operators_count += 1
        else:
            operands_count += 1
        index -= 1

    tmp1 = expression[:index + 1]
    tmp2 = expression[index + 1:]
    pool = mp.Pool(2)
    expr1 = pool.apply_async(postfix_evaluation, [tmp1])
    expr2 = pool.apply_async(postfix_evaluation, [tmp2])

    expr1 = expr1.get()
    expr2 = expr2.get()

    pool.close()
    pool.join()
    return postfix_evaluation([expr1, expr2, last_operator])

def postfix_transform(expression):
    postfix = []
    stack = []
    dot = '.'
    left_par = '('
    right_par = ')'
    prec = {'*': 3, '/':3, '+':2, '-':2, '(':1}
    expression.replace(' ', '')
    is_negative = False

    for i in range(len(expression)):
        if expression[i].isdigit():
            if i > 0 and (expression[i - 1].isdigit() or expression[i-1] == dot):
                postfix[-1] = postfix[-1] + expression[i]
            else:
                digit = expression[i]
                if is_negative:
                    is_negative = False
                    digit = '-' + digit
                postfix.append(digit)

        elif expression[i] == dot:
            if not expression[i-1].isdigit() or not expression[i+1].isdigit():
                raise Exception("bad dot placement")
            postfix[-1] = postfix[-1] + dot

        elif is_negative:
            pass

        elif expression[i] in operators:
            while len(stack) > 0 and prec[expression[i]] <= prec[stack[-1]]:
                postfix.append(stack.pop())
            stack.append(expression[i])

        elif expression[i] == left_par:
            if expression[i+1] in '+*/':
                raise Exception('invalid operator placement')
            if expression[i+1] == '-':
                is_negative = True
            stack.append(expression[i])

        elif expression[i] == right_par:
            if expression[i-1] in operators:
                raise Exception('invalid operator placement')
            try:
                o = stack.pop()
                while o != left_par:
                    postfix.append(o)
                    o = stack.pop()
            except:
                raise Exception('Unclosed parenthisis')
        else:
            raise Exception('Character not allowed')

    while len(stack) > 0:
        o = stack.pop()
        if o == left_par:
            raise Exception('Unclosed parenthisis')
        postfix.append(o)

    if len(postfix) % 2 == 0:
        raise Exception('invalid number of operators')
    return postfix

def is_digit(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

