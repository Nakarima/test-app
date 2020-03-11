import multiprocessing as mp

def calc(expression):
    try:
        res = expr_evaluation(postfix_transform(expression))
        return res
    except Exception as e:
        raise Exception(str(e))

def postfix_evaluation(expression):
    if len(expression) == 1:
        return expression[0]

    def is_digit(x):
        try:
            float(x)
            return True
        except ValueError:
            return False

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
    return str(stack[0])

def expr_evaluation(expression):
    if len(expression) < 7:
        return postfix_evaluation(expression)

    last_operator = expression.pop()
    operands_count = 0
    operators_count = 1
    index = len(expression) - 1

    while operators_count != operands_count:
        if expression[index] in '*-/+':
            operators_count += 1
        else:
            operands_count += 1
        index -= 1

    tmp1 = expression[:index + 1]
    tmp2 = expression[index + 1:]
    pool = mp.Pool(2)
    #find way for recurrent processes
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
    operators = '+-/*'
    prec = {'*': 3, '/':3, '+':2, '-':2, '(':1}
    expression.replace(' ', '')

    for i in range(len(expression)):
        if expression[i].isdigit():
            if i > 0 and expression[i - 1].isdigit():
                postfix[-1] = postfix[-1] + expression[i]
            else:
                postfix.append(expression[i])

        elif expression[i] in operators:
            while len(stack) > 0 and prec[expression[i]] <= prec[stack[-1]]:
                postfix.append(stack.pop())
            stack.append(expression[i])

        elif expression[i] == '(':
            if expression[i+1] in operators:
                raise Exception('invalid operator placement')
            stack.append(expression[i])

        elif expression[i] == ')':
            if expression[i-1] in operators:
                raise Exception('invalid operator placement')
            o = stack.pop()
            try:
                while o != '(':
                    postfix.append(o)
                    o = stack.pop()
            except:
                raise Exception('Unclosed parenthisis')
            if len(stack) > 0 and stack[-1] in operators:
                postfix.append(stack.pop())
        else:
            raise Exception('Character not allowed')

    while len(stack) > 0:
        o = stack.pop()
        if o == "(":
            raise Exception('Unclosed parenthisis')
        postfix.append(o)
    
    if len(postfix) % 2 == 0:
        raise Exception('invalid number of operators')
    return postfix
