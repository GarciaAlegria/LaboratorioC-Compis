from readyalex import read_yalex

def getPrecedence(ope):
    precedencia = {'(': 1, '|': 2, '.': 3, '+': 4, '?': 4, '*': 4}
    if ope not in precedencia:
        return 5
    return precedencia[ope]

def formatear_regex(regex):
    all_operators = ['|', '+', '?', '*']
    binary_operators = ['|']
    res = ''

    for i in range(len(regex)):
        c1 = regex[i]

        if i + 1 < len(regex):
            c2 = regex[i + 1]

            res += str(c1)  # Convertir c1 a cadena antes de concatenar
            if c1 != '(' and c2 != ')' and c2 not in all_operators and c1 not in binary_operators:
                res += '.'
    
    res += str(regex[-1])  # Convertir el último elemento a cadena antes de concatenar
    return res


def infix_to_postfix(regex):
    stack = []
    postfix = ''
    regexp = formatear_regex(regex)
    print("formatear regex:")
    print(regexp)

    for c in regexp:
        if c == '(':
            stack.append(c)
        elif c == ')':
            while stack[-1] != '(':
                postfix += stack.pop()
            stack.pop()
        else:
            while len(stack) > 0:
                peekedChar = stack[-1]
                peekedCharPrecedence = getPrecedence(peekedChar)
                currentCharPrecedence = getPrecedence(c)

                if peekedCharPrecedence >= currentCharPrecedence:
                    postfix += stack.pop()
                else:
                    break

            stack.append(c)

    while len(stack) > 0:
        postfix += stack.pop()
    return postfix