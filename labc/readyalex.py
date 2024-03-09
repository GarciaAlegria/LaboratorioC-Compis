def read_yalex(yalex_file):
    # Listas para almacenar funciones y expresiones regulares
    functions = []  # Lista para almacenar las definiciones de funciones
    clean_functions = []  # Lista para almacenar las definiciones de funciones limpias
    regex = []  # Lista para almacenar las expresiones regulares
    clean_regex_expression = []  # Lista para almacenar las expresiones regulares limpias
    reserved_word = ""  # Palabra reservada temporal

    # Revisar errores de cierre de corchetes
    def check_brackets(line, line_number):
        if line.count("[") != line.count("]"):
            raise ValueError(f"Error en línea {line_number}: Error de cierre de corchetes")

    # Revisar errores de comillas simples y dobles
    def check_quotes(line, line_number):
        if line.count("'") % 2 != 0 or line.count('"') % 2 != 0:
            raise ValueError(f"Error en línea {line_number}: Error de comillas")

    # Sección de rule vacía
    def check_empty_rule(line, line_number):
        if line.startswith("rule") and not any(c.isalnum() for c in line):
            raise ValueError(f"Error en línea {line_number}: Sección 'rule' vacía")

    # Abrir el archivo y leerlo línea por línea
    with open(yalex_file, "r") as yal:
        active_elements = False
        for line_number, line in enumerate(yal, start=1):
            # Procesamiento de las líneas del archivo
            check_brackets(line, line_number)
            check_quotes(line, line_number)
            check_empty_rule(line, line_number)
            
            if active_elements:
                temporary_reserved_word = ""
                # Leer cada carácter de la línea
                for x in line:
                    if x != " ":
                        if x != "\n":
                            if x != "'":
                                temporary_reserved_word += x
                            if x == "|":
                                regex.append(temporary_reserved_word)
                                temporary_reserved_word = ""
                        else:
                            regex.append(temporary_reserved_word)
            if line.startswith("let"):
                if "=" not in line:
                    raise ValueError(f"Error en línea {line_number}: Falta el símbolo '=' en la declaración 'let'")
                elif len(line.split("=")) != 2:
                    raise ValueError(f"Error en línea {line_number}: Declaración 'let' incorrecta")
                elif len(line.split("=")[1].strip()) == 0:
                    raise ValueError(f"Error en línea {line_number}: La declaración 'let' está vacía")
                functions.append(line[4:-1])  # Agregar la definición de la función a la lista de funciones
            if line.startswith("rule"):
                active_elements = True  # Activar la bandera para procesar las expresiones regulares

    if active_elements and not regex:  # Verificar si se espera una expresión regular pero no se encuentra ninguna
        raise ValueError("No se encontraron expresiones regulares después de 'rule'")

    # Procesamiento de expresiones regulares
    for x in range(len(regex)):
        temporary_reserved_word = ""
        for l in regex[x]:
            temporary_reserved_word += l
            if "{" in temporary_reserved_word:
                temporary_reserved_word = temporary_reserved_word[:-1]
                break
            if "(*" in temporary_reserved_word:
                temporary_reserved_word = temporary_reserved_word[:-2]
                break

        # Actualizar la lista regex con el valor modificado
        regex[x] = temporary_reserved_word

    # Procesamiento de expresiones regulares
    clean_regex_expression = []
    for x in regex:
        if len(x) != 0:
            if x.count('"') == 2:
                x = x[1:-1]
            clean_regex_expression.append(x)

    # Procesamiento de funciones
    for f in functions:
        deletable_array = []  # Lista para almacenar los tokens de la función
        temp_expression = []  # Lista temporal para almacenar la definición de la función
        nombre, definition = f.split("=")
        nombre = nombre.strip()  # Limpiar el nombre de la función
        definition = definition.strip()  # Limpiar la definición de la función
        temp_expression.append(nombre)
        reserved_word = ""
        if definition[0] == "[":
            definition = definition[1:-1]
            for x in definition:
                reserved_word += x
                if reserved_word[0] == '"' or reserved_word[0] == "'":
                    if reserved_word.count("'") == 2:
                        reserved_word = reserved_word[1:-1]
                        # Manejo de caracteres especiales
                        if len(reserved_word) == 2:
                            if reserved_word == "\s":
                                reserved_word = bytes(" ", "utf-8").decode(
                                    "unicode_escape"
                                )
                            else:
                                reserved_word = bytes(
                                    reserved_word, "utf-8"
                                ).decode("unicode_escape")
                            deletable_array.append(ord(reserved_word))
                        else:
                            if reserved_word == " ":
                                reserved_word = bytes(" ", "utf-8").decode(
                                    "unicode_escape"
                                )
                                deletable_array.append(ord(reserved_word))
                            else:
                                deletable_array.append(ord(reserved_word))
                        reserved_word = ""
                    if reserved_word.count('"') == 2:
                        reserved_word = reserved_word[1:-1]
                        temporary_reserved_word = ""
                        # Manejo de caracteres de escape (\)
                        if chr(92) in reserved_word:
                            for y in reserved_word:
                                temporary_reserved_word += y
                                if temporary_reserved_word.count(chr(92)) == 2:
                                    if temporary_reserved_word[:-1] == "\s":
                                        temp_reserved_word = " "
                                    else:
                                        temp_reserved_word = (
                                            temporary_reserved_word[:-1]
                                        )
                                    reserved_word = bytes(
                                        temp_reserved_word, "utf-8"
                                    ).decode("unicode_escape")
                                    deletable_array.append(ord(reserved_word))
                                    temporary_reserved_word = (
                                        temporary_reserved_word[2:]
                                    )
                            if len(temporary_reserved_word) != 0:
                                if temporary_reserved_word == "\s":
                                    temp_reserved_word = " "
                                else:
                                    temp_reserved_word = temporary_reserved_word
                                reserved_word = bytes(
                                    temp_reserved_word, "utf-8"
                                ).decode("unicode_escape")
                                deletable_array.append(ord(reserved_word))
                        else:
                            reserved_word = list(reserved_word)
                            for w in range(len(reserved_word)):
                                reserved_word[w] = ord(reserved_word[w])
                            deletable_array.extend(reserved_word)
                else:
                    deletable_array.append(reserved_word)
                    reserved_word = ""
        else:
            tokens = []
            token_actual = ""
            # Procesamiento de la definición de la función
            for char in definition:
                if "]" in token_actual:
                    word = ""
                    array = []
                    array.append("(")
                    token_actual = token_actual[1:-1]
                    for tok in token_actual:
                        word += tok
                        if word.count("'") == 2:
                            word = ord(word[1:-1])
                            array.append(word)
                            array.append("|")
                            word = ""
                    array[len(array) - 1] = ")"
                    tokens.extend(array)
                    token_actual = ""
                if token_actual.count("'") == 2:
                    if "[" not in token_actual:
                        token_actual = token_actual[1:-1]
                        if token_actual == 'E':
                            token_actual = ord(token_actual)  # Convertir 'E' a ASCII
                        tokens.append(token_actual)
                        token_actual = ""
                if char in ("(", ")", "*", "?", "+", "|", "·"):
                    if "'" not in token_actual:
                        if token_actual:
                            if len(token_actual) == 1:
                                token_actual = ord(token_actual)
                            tokens.append(token_actual)
                            token_actual = ""
                        tokens.append(char)
                    else:
                        token_actual += char
                else:
                    if char == '_':
                        for i in range(32, 127):
                            tokens.append(i)
                            tokens.append("|")
                    token_actual += char
            if token_actual:
                tokens.append(token_actual)
            deletable_array.extend(tokens)
        temp_expression.append(deletable_array)
        clean_functions.append(temp_expression)

    # Procesamiento adicional de funciones
    for x in range(len(clean_functions)):
        isFunc = True
        for c in ["+", "*", "(", ")", "?", "|"]:
            if c in clean_functions[x][1]:
                isFunc = False
        if isFunc == False:
            temp_expression = []
            for y in clean_functions[x][1]:
                temp_expression.append(y)
                temp_expression.append("·")
            for z in range(len(temp_expression)):
                if temp_expression[z] == "(":
                    if temp_expression[z + 1] == "·":
                        temp_expression[z + 1] = ""
                if temp_expression[z] == ")":
                    if temp_expression[z - 1] == "·":
                        temp_expression[z - 1] = ""
                if temp_expression[z] == "*":
                    if temp_expression[z - 1] == "·":
                        temp_expression[z - 1] = ""
                if temp_expression[z] == "|":
                    if temp_expression[z - 1] == "·":
                        temp_expression[z - 1] = ""
                    if temp_expression[z + 1] == "·":
                        temp_expression[z + 1] = ""
                if temp_expression[z] == "+":
                    if temp_expression[z - 1] == "·":
                        temp_expression[z - 1] = ""
                if temp_expression[z] == "?":
                    if temp_expression[z - 1] == "·":
                        temp_expression[z - 1] = ""
            temp_expression = [element for element in temp_expression if element != ""]
            clean_functions[x][1] = temp_expression[:-1]
        else:
            ascii_array = []
            newString_Array = []
            if "-" in clean_functions[x][1]:
                for z in range(len(clean_functions[x][1])):
                    if clean_functions[x][1][z] == "-":
                        for i in range(
                            clean_functions[x][1][z - 1],
                            clean_functions[x][1][z + 1] + 1,
                        ):
                            ascii_array.append(i)
                for i in ascii_array:
                    newString_Array.append(i)
                clean_functions[x][1] = newString_Array
            newString_Array = []
            for y in clean_functions[x][1]:
                newString_Array.append(y)
                newString_Array.append("|")
            newString_Array = newString_Array[:-1]
            clean_functions[x][1] = newString_Array

    # Agregar paréntesis a las funciones
    for func in clean_functions:
        func[1] = ["("] + func[1] + [")"]

    # Convertir caracteres individuales a códigos ASCII
    functionNames = [x[0] for x in clean_functions] + ["|"]
    clean_regex_expression = [
        ord(x) if len(x) == 1 and x not in functionNames else x
        for x in clean_regex_expression
    ]

    temporalNewRegex = []
    # Agregar concatenación y etiquetas a las expresiones regulares
    for x in clean_regex_expression:
        if x != "|":
            temporalNewRegex.append("(")
            temporalNewRegex.append(x)
            temporalNewRegex.append("·")
            temporalNewRegex.append("#" + str(x))
            temporalNewRegex.append(")")
        else:
            temporalNewRegex.append(x)

    clean_regex_expression = temporalNewRegex

    # Reemplazar referencias a funciones en expresiones regulares
    def replace_regex(regex, functions):
        final_regex = []
        for r in regex:
            if r in functions:
                final_regex.extend(replace_regex(functions[r], functions))
            else:
                final_regex.append(r)
        return final_regex

    final_regex = replace_regex(clean_regex_expression, dict(clean_functions))

    return final_regex
