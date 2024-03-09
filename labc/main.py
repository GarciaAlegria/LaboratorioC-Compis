import readyalex as read
import shuntingyard as sy
from arbol import SyntacticTree

def main():
    yalex_file = 'slr-4.yal' 
    content = read.read_yalex(yalex_file)
    if content:
        print("====================================================")
        print("Reguex del Archivo Yalex ==========================")
        print(content)
        print("====================================================")
        print("====================================================")
        postfix = sy.shunting_yard(content)
        print("Postfix de la regex ================================")
        print(postfix)
        print("====================================================")
        print("====================================================")
        print("Generando árbol de expresión...")
        tree = SyntacticTree(yalex_file)
        tree.tree_construction(postfix)
        tree.visualize_tree()
        result = tree.left_most()
        print("Árbol de expresión generado y guardado como 'expression_tree.png'")
        print("=====================================================")
        print("=====================================================")

if __name__ == "__main__":
    main()