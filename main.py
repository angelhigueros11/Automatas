# Proyecto teoria de la computacion
# Mariana David 201055
# Angel Higueros 20460
# Fredy Velasquez 201011


from Automatas import *
import sys


def main():
    # aqui se define la cadena con la que se trabaja
    inp = "(01*1)*1"

    # Operaciones con los grafos
    nfaObj = NFAfromRegex(inp)
    nfa = nfaObj.getNFA()
    dfaObj = DFAfromNFA(nfa)
    dfa = dfaObj.getDFA()
    minDFA = dfaObj.getMinimisedDFA()

    # Despliegue de los grafos
    print("\n:: AFN:: ")
    nfaObj.displayNFA()
    print("\n:: AFD :: ")
    dfaObj.displayDFA()
    print("\n:: AFD minimizado ::")
    dfaObj.displayMinimisedDFA()


if __name__ == '__main__':
    t = time.time()
    main()

    # try:
    # except BaseException as e:
    #     print("\n[!] Error")
    print("\n[!] Tiempo: ", time.time() - t, " segundos")
