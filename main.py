# Proyecto 1 - Teoria de la computación
# Integrantes:
#     - Mariana David 
#     - Fredy Velasquez
#     - Angel Higueros


from automata import *
from postfix_nfa import *
from afn_afd import *
import sys

def main():
    r = input()
    w = input()

    # Convertir regex a un AFN
    afn_generado = Regex_AFN(r)
    afn = afn_generado.getAFN()

    # Convertir AFN en AFD
    afd_generado = AFN_AFD(nfa)
    afd = afd_generado.getDFA()

    # Minimizar el AFD
    minDFA = afd_generado.getAFDminimizado()

    # Mostrar el AFN, el AFD y el AFD minimizado
    print ("\n:: AFN :: ")
    afn_generado.displayNFA()

    print ("\n:: AFD :: ")
    afd_generado.displayDFA()

    print ("\n:: AFD MINIMIZADO ::")
    afd_generado.displayMinimisedDFA()

    # Mostrar si la cadena pertenece a w pertenece al leguaje L(r)

    # Generar archivo excel


def expresion_postfix(regex):
    regex = regex.replace('?','|ε')
    while('+' in regex):
        print(regex)
        index = regex.index('+')
        if(index>0):
            if(regex[index-1]!=')'):
                regex = regex[:index] + '(' + regex[index-1] + ")*" + regex[index+1:]
            else:
                new_index = index
                while(regex[new_index]!='('):
                    new_index -= 1
                    if(index==0):
                        raise SyntaxError        
                regex = regex[:new_index] + regex[new_index:index] + regex[new_index:index]  + "*"  + regex[index+1:]
        else:
            raise SyntaxError
    return regex


if __name__  ==  '__main__':
    t = time.time()
    try:
        main()
    except BaseException as e:
        print ("\nFailure:", e)
    print ("\nExecution time: ", time.time() - t, "seconds")
