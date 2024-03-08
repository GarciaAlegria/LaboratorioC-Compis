import pydotplus
from collections import deque

class SyntacticTree:
    def __init__(self, title):
        self.root = None  # Nodo raíz del árbol
        self.title = title  # Título del árbol

    class Node:
        def __init__(self, value):
            self.data = value  # Valor almacenado en el nodo
            self.left = None   # Referencia al nodo hijo izquierdo
            self.right = None  # Referencia al nodo hijo derecho

    def tree_construction(self, postfix):
        print("Contenido de postfix:", postfix)  # Imprime el contenido del postfix
        stack = []  # Pila para almacenar nodos temporales durante la construcción del árbol
        for symbol in postfix:
            print("Procesando símbolo:", symbol)  # Imprime el símbolo que se está procesando
            if str(symbol) not in "|*·+?":
                if type(symbol) == int:
                    symbol = str(symbol)
                node = self.Node(symbol)  # Crea un nodo con el símbolo
                stack.append(node)  # Agrega el nodo a la pila
                print("Stack después de agregar nodo:", [n.data for n in stack])  # Imprime el estado actual de la pila
            elif symbol == "|":
                node = self.Node(symbol)  # Crea un nodo para el operador '|'
                node.right = stack.pop()  # Asigna el último nodo de la pila como hijo derecho
                node.left = stack.pop()   # Asigna el penúltimo nodo de la pila como hijo izquierdo
                stack.append(node)        # Agrega el nodo con el operador a la pila
                print("Stack después de agregar operador:", [n.data for n in stack])  # Imprime el estado actual de la pila
            elif symbol == "·":
                if len(stack) < 2:
                    raise ValueError("No hay suficientes elementos en la pila para el operador:", symbol)
                node = self.Node(symbol)  # Crea un nodo para el operador '·'
                node.right = stack.pop()  # Asigna el último nodo de la pila como hijo derecho
                node.left = stack.pop()   # Asigna el penúltimo nodo de la pila como hijo izquierdo
                stack.append(node)        # Agrega el nodo con el operador a la pila
                print("Stack después de agregar operador:", [n.data for n in stack])  # Imprime el estado actual de la pila
            elif symbol in "*+?":
                node = self.Node(symbol)  # Crea un nodo para los operadores '*', '+', '?'
                node.left = stack.pop()   # Asigna el último nodo de la pila como hijo izquierdo
                stack.append(node)        # Agrega el nodo con el operador a la pila
                print("Stack después de agregar operador:", [n.data for n in stack])  # Imprime el estado actual de la pila
        self.root = stack.pop()  # El último nodo restante en la pila es la raíz del árbol

    def left_most(self):
        if self.root is None:
            return []
        queue = deque([self.root])  # Cola para recorrer los nodos en orden de izquierda a derecha
        result = []
        while queue:
            node = queue.popleft()
            result.append(node.data)  # Agrega el valor del nodo al resultado
            if node.left is not None:
                queue.append(node.left)  # Agrega el hijo izquierdo a la cola
            if node.right is not None:
                queue.append(node.right)  # Agrega el hijo derecho a la cola
        return result

    def generate_dot(self, node, graph):
        if node is not None:
            graph.add_node(pydotplus.Node(str(id(node)), label=node.data))  # Añade el nodo al gráfico
            if node.left is not None:
                graph.add_edge(pydotplus.Edge(str(id(node)), str(id(node.left))))  # Añade un borde del nodo al hijo izquierdo
                self.generate_dot(node.left, graph)  # Llama recursivamente a la función para el hijo izquierdo
            if node.right is not None:
                graph.add_edge(pydotplus.Edge(str(id(node)), str(id(node.right))))  # Añade un borde del nodo al hijo derecho
                self.generate_dot(node.right, graph)  # Llama recursivamente a la función para el hijo derecho

    def visualize_tree(self):
        description = "Syntactic Tree of " + self.title
        graph = pydotplus.Dot(comment=description)  # Crea un gráfico
        final_node = self.root
        self.generate_dot(final_node, graph)  # Genera el gráfico del árbol
        graph.write_png("SyntacticTree_of_" + self.title + ".png")  # Guarda el gráfico como imagen PNG
