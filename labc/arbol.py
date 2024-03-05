import pydotplus
from collections import deque

class SyntacticTree:
    def __init__(self, title):
        self.root = None
        self.title = title

    class Node:
        def __init__(self, value):
            self.data = value
            self.left = None
            self.right = None

    def tree_construction(self, postfix):
        print("Contenido de postfix:", postfix) 
        stack = []
        for symbol in postfix:
            print("Procesando símbolo:", symbol)
            if str(symbol) not in "|*·+?":
                if type(symbol) == int:
                    symbol = str(symbol)
                node = self.Node(symbol)
                stack.append(node)
                print("Stack después de agregar nodo:", [n.data for n in stack])
            elif symbol == "|":
                node = self.Node(symbol)
                node.right = stack.pop()
                node.left = stack.pop()
                stack.append(node)
                print("Stack después de agregar operador:", [n.data for n in stack])
            elif symbol == "·":
                if len(stack) < 2:
                    raise ValueError("No hay suficientes elementos en la pila para el operador:", symbol)
                node = self.Node(symbol)
                node.right = stack.pop()
                node.left = stack.pop()
                stack.append(node)
                print("Stack después de agregar operador:", [n.data for n in stack])
            elif symbol in "*+?":
                node = self.Node(symbol)
                node.left = stack.pop()
                stack.append(node)
                print("Stack después de agregar operador:", [n.data for n in stack])
                
        self.root = stack.pop()




    def left_most(self):
        if self.root is None:
            return []
        queue = deque([self.root])
        result = []
        while queue:
            node = queue.popleft()
            result.append(node.data)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        return result

    def generate_dot(self, node, graph):
        if node is not None:
            graph.add_node(pydotplus.Node(str(id(node)), label=node.data))
            if node.left is not None:
                graph.add_edge(pydotplus.Edge(str(id(node)), str(id(node.left))))
                self.generate_dot(node.left, graph)
            if node.right is not None:
                graph.add_edge(pydotplus.Edge(str(id(node)), str(id(node.right))))
                self.generate_dot(node.right, graph)

    def visualize_tree(self):
        description = "Syntactic Tree of " + self.title
        graph = pydotplus.Dot(comment=description)
        final_node = self.root
        self.generate_dot(final_node, graph)
        graph.write_png("SyntacticTree_of_" + self.title + ".png")
