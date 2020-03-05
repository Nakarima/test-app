def calc(expression):
    try:
        postfix_expr = postfix_transform(expression)
        return str(postfix_evaluation(postfix_expr))
    except Exception as e:
        raise Exception(str(e))

def postfix_evaluation(expression):
    stack = []
    operators = {'+': lambda x, y: x + y,
                 '-': lambda x, y: x - y,
                 '*': lambda x, y: x * y,
                 '/': lambda x, y: x / y}
    for symbol in expression:
        if symbol.isdigit():
            stack.append(symbol)
        else:
            s2 = int(stack.pop())
            s1 = int(stack.pop())
            stack.append(int(operators[symbol](s1,s2)))
    print(stack[0])
    return stack[0]

def postfix_transform(expression):
    postfix = []
    stack = []
    funcs = '+-/*'
    prec = {'*': 3, '/':3, '+':2, '-':2, '(':1}
    for i in range(len(expression)):
        if expression[i].isdigit():
            if i > 0 and expression[i - 1].isdigit():
                postfix[-1] = postfix[-1] + expression[i]
            else:
                postfix.append(expression[i])

        elif expression[i] in funcs:
            while len(stack) > 0 and prec[expression[i]] <= prec[stack[-1]]:
                postfix.append(stack.pop())
            stack.append(expression[i])

        elif expression[i] == '(':
            stack.append(expression[i])

        elif expression[i] == ')':
            o = stack.pop()
            try:
                while o != '(':
                    postfix.append(o)
                    o = stack.pop()
            except:
                raise Exception('Unclosed parenthisis')
            if len(stack) > 0 and stack[-1] in funcs:
                postfix.append(stack.pop())
        else:
            raise Exception('Character not allowed')

    while len(stack) > 0:
        postfix.append(stack.pop())

    return postfix
