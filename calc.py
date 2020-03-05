def calc(expression):
    try:
        return postfix_transform(expression)
    except Exception as e:
        raise Exception(str(e))




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
            if len(stack) > 0 and stack[-1] in funcs: #not sure about it
                postfix.append(stack.pop())
        else:
            raise Exception('Character not allowed')

    while len(stack) > 0:
        postfix.append(stack.pop())

    return ''.join(postfix)
