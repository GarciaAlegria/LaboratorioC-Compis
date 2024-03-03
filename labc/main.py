import readyalex as read
import shuntingyard as sy
#from arbol import SyntacticTree
from arbol import construir_arbol, dibujar_arbol
#import time

def main():
    yalex_file = 'slr-1.yal' 
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
        print("====================================================")
        print("Generando árbol de expresión...")
        arbol = construir_arbol(postfix)
        dibujar_arbol(arbol, "arbol_sintactico.png")
        print("Árbol de expresión generado y guardado como 'arbol_sintactico.png'")
        print("=====================================================")
        print("=====================================================")


if __name__ == "__main__":
    main()