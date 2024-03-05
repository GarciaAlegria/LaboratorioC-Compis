def shunting_yard(regex):
    # Definir los operadores y paréntesis
    PIPE = '|'
    STAR = '*'
    PLUS = '+'
    QUESTION = '?'
    CONCAT = '·'
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    # Asignar precedencias a los operadores
    OPERATORS = {PIPE: 1, CONCAT: 2, QUESTION: 3, STAR: 3, PLUS: 3}

    # Inicializar una pila y una lista de salida
    stack = []
    output = []

    # Iterar sobre cada token en la expresión regular
    for token in regex:
        # Si el token es un operador
        if token in OPERATORS:
            # Mientras la pila no esté vacía y el operador en la cima de la pila no sea un paréntesis izquierdo
            # y la precedencia del operador actual sea menor o igual que la precedencia del operador en la cima de la pila
            while stack and stack[-1] != LEFT_PAREN and OPERATORS[token] <= OPERATORS.get(stack[-1], 0):
                # Sacar el operador de la pila y agregarlo a la lista de salida
                output.append(stack.pop())
            # Agregar el operador actual a la pila
            stack.append(token)
        # Si el token es un paréntesis izquierdo
        elif token == LEFT_PAREN:
            # Agregar el paréntesis izquierdo a la pila
            stack.append(token)
        # Si el token es un paréntesis derecho
        elif token == RIGHT_PAREN:
            # Mientras la pila no esté vacía y el operador en la cima de la pila no sea un paréntesis izquierdo
            while stack and stack[-1] != LEFT_PAREN:
                # Sacar el operador de la pila y agregarlo a la lista de salida
                output.append(stack.pop())
            # Si la pila no está vacía y el operador en la cima de la pila es un paréntesis izquierdo
            if stack and stack[-1] == LEFT_PAREN:
                # Sacar el paréntesis izquierdo de la pila
                stack.pop()
        # Si el token es un carácter literal
        else:
            # Agregar el carácter literal a la lista de salida
            output.append(token)

    # Vaciar la pila y agregar cualquier operador restante a la lista de salida
    while stack:
        output.append(stack.pop())

    # Devolver la lista de salida que representa la expresión regular en notación posfija
    return output
