from os import popen
import time

# Clase que representa a un automata
class Automata:

    # Metodos y asigno en la clase
    def __init__(self, language=set(['0', '1'])):
        self.states = set()
        self.startstate = None
        self.finalstates = []
        self.transitions = dict()
        self.language = language
    # Definir epsilon

    @staticmethod
    def epsilon():
        return ":e:"
    # construyo el estado inicial

    def setEstadoInicial(self, state):
        self.startstate = state
        self.states.add(state)
    # Agrego los estados finales

    def agregarEstadosFinales(self, state):
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.finalstates:
                self.finalstates.append(s)

    # Agregar las transiciones originadas de la regexp
    def agregarTransiciones(self, fromstate, tostate, inp):
        if isinstance(inp, str):
            inp = set([inp])
        self.states.add(fromstate)
        self.states.add(tostate)
        if fromstate in self.transitions:  # si se encuentra en las transiciones
            if tostate in self.transitions[fromstate]:
                self.transitions[fromstate][tostate] = self.transitions[fromstate][tostate].union(
                    inp)
            else:
                self.transitions[fromstate][tostate] = inp
        else:
            self.transitions[fromstate] = {tostate: inp}
    # agrego la transicion

    def agregarTransiciones_dict(self, transitions):
        for fromstate, tostates in transitions.items():
            for state in tostates:
                self.agregarTransiciones(fromstate, state, tostates[state])
    # obtengo las transiciones

    def obtenerTransiciones(self, state, key):
        if isinstance(state, int):
            state = [state]
        tr = set()
        for st in state:
            if st in self.transitions:
                for tns in self.transitions[st]:
                    if key in self.transitions[st][tns]:
                        tr.add(tns)
        return tr
    # obtego todos los estados en E

    def obtenerEstadosE(self, findstate):
        estados = set()
        states = set([findstate])
        while len(states) != 0:
            state = states.pop()
            estados.add(state)
            if state in self.transitions:
                for tns in self.transitions[state]:
                    if Automata.epsilon() in self.transitions[state][tns] and tns not in estados:
                        states.add(tns)
        return estados
    # Funcion que me ayuda a mostrar todo con lo que estoy trabajando

    def display(self):
        print("ESTADOS:", self.states)
        print("ESTADOS FINALES: ", self.finalstates)
        print("TRANSICIONES:")
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                for letra in tostates[state]:
                    print("  ", fromstate, "->", state, "en '"+letra+"'")


    # Construyo desde el numero

    def automataNumeros(self, startnum):
        translations = {}
        for i in list(self.states):
            translations[i] = startnum
            startnum += 1
        rebuild = Automata(self.language)
        rebuild.setEstadoInicial(translations[self.startstate])
        rebuild.agregarEstadosFinales(translations[self.finalstates[0]])
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                rebuild.agregarTransiciones(
                    translations[fromstate], translations[state], tostates[state])
        return [rebuild, startnum]
    # Construyo desde los estados equivalentees existentes

    def automataEstados(self, equivalente, pos):
        rebuild = Automata(self.language)
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                rebuild.agregarTransiciones(
                    pos[fromstate], pos[state], tostates[state])
        rebuild.setEstadoInicial(pos[self.startstate])
        for s in self.finalstates:
            rebuild.agregarEstadosFinales(pos[s])
        return rebuild


# Clase para construir las estructuras basicas del nfa
class BuildAutomata:
    # Creo unos estados y transiciones de default para hacer pruebas
    @staticmethod
    def simbolos(inp):
        state1 = 1
        state2 = 2
        basic = Automata()
        basic.setEstadoInicial(state1)
        basic.agregarEstadosFinales(state2)
        basic.agregarTransiciones(1, 2, inp)
        return basic
    # Sigo desarrollando la estructura

    @staticmethod
    def simboloMas(a, b):
        [a, m1] = a.automataNumeros(2)
        [b, m2] = b.automataNumeros(m1)
        state1 = 1
        state2 = m2
        plus = Automata()
        plus.setEstadoInicial(state1)
        plus.agregarEstadosFinales(state2)
        plus.agregarTransiciones(plus.startstate, a.startstate, Automata.epsilon())
        plus.agregarTransiciones(plus.startstate, b.startstate, Automata.epsilon())
        plus.agregarTransiciones(
            a.finalstates[0], plus.finalstates[0], Automata.epsilon())
        plus.agregarTransiciones(
            b.finalstates[0], plus.finalstates[0], Automata.epsilon())
        plus.agregarTransiciones_dict(a.transitions)
        plus.agregarTransiciones_dict(b.transitions)
        return plus
    # Estructura del dot para crear el grafo

    @staticmethod
    def simboloPunto(a, b):
        [a, m1] = a.automataNumeros(1)
        [b, m2] = b.automataNumeros(m1)
        state1 = 1
        state2 = m2-1
        dot = Automata()
        dot.setEstadoInicial(state1)
        dot.agregarEstadosFinales(state2)
        dot.agregarTransiciones(a.finalstates[0], b.startstate, Automata.epsilon())
        dot.agregarTransiciones_dict(a.transitions)
        dot.agregarTransiciones_dict(b.transitions)
        return dot
    # Estrucutra para el comienzo

    @staticmethod
    def simboloEstrella(a):
        [a, m1] = a.automataNumeros(2)
        state1 = 1
        state2 = m1
        star = Automata()
        star.setEstadoInicial(state1)
        star.agregarEstadosFinales(state2)
        star.agregarTransiciones(star.startstate, a.startstate, Automata.epsilon())
        star.agregarTransiciones(
            star.startstate, star.finalstates[0], Automata.epsilon())
        star.agregarTransiciones(
            a.finalstates[0], star.finalstates[0], Automata.epsilon())
        star.agregarTransiciones(a.finalstates[0], a.startstate, Automata.epsilon())
        star.agregarTransiciones_dict(a.transitions)
        return star


# Clase para comstrior DFA desde un NFA y minimizarlo de una vez
class DFAfromNFA:
    # Inicializo lo que voy a utilizar
    def __init__(self, nfa):
        self.buildDFA(nfa)
        self.minimise()

    # Obtengo las cosas que voy a utilizar

    def getDFA(self):
        return self.dfa

    def getMinimisedDFA(self):
        return self.minDFA

    def displayDFA(self):
        self.dfa.display()

    def displayMinimisedDFA(self):
        self.minDFA.display()

    # Construyo paso a paso el DFA
    def buildDFA(self, nfa):
        estados = dict()
        eclose = dict()
        count = 1
        state1 = nfa.obtenerEstadosE(nfa.startstate)
        eclose[nfa.startstate] = state1
        dfa = Automata(nfa.language)
        dfa.setEstadoInicial(count)
        states = [[state1, count]]
        estados[count] = state1
        count += 1
        while len(states) != 0:
            [state, fromindex] = states.pop()
            for letra in dfa.language:
                tr = nfa.obtenerTransiciones(state, letra)
                for s in list(tr)[:]:
                    if s not in eclose:
                        eclose[s] = nfa.obtenerEstadosE(s)
                    tr = tr.union(eclose[s])
                if len(tr) != 0:
                    if tr not in estados.values():
                        states.append([tr, count])
                        estados[count] = tr
                        toindex = count
                        count += 1
                    else:
                        toindex = [k for k, v in estados.iteritems()
                                   if v == tr][0]
                    dfa.agregarTransiciones(fromindex, toindex, letra)
        for value, state in estados.iteritems():
            if nfa.finalstates[0] in state:
                dfa.agregarEstadosFinales(value)
        self.dfa = dfa

    # Aceptar el string y verificar
    def aceptarStrings(self, string):
        actual = self.dfa.startstate
        for ch in string:
            if ch == ":e:":
                continue
            st = list(self.dfa.obtenerTransiciones(actual, ch))
            if len(st) == 0:
                return False
            actual = st[0]
        if actual in self.dfa.finalstates:
            return True
        return False
    # Funcion que lo minimiza

    def minimise(self):
        states = list(self.dfa.states)
        n = len(states)
        stack = dict()
        count = 1
        automata_final = []
        equivalente = dict(zip(range(len(states)), [{s} for s in states]))
        pos = dict(zip(states, range(len(states))))
        for i in range(n-1):
            for j in range(i+1, n):
                if not ([states[i], states[j]] in automata_final or [states[j], states[i]] in automata_final):
                    eq = 1
                    to = []
                    for letra in self.dfa.language:
                        s1 = self.dfa.obtenerTransiciones(states[i], letra)
                        s2 = self.dfa.obtenerTransiciones(states[j], letra)
                        if len(s1) != len(s2):
                            eq = 0
                            break
                        if len(s1) > 1:
                            raise BaseException(
                                "Existen multiples transformaciones en el DFA")
                        elif len(s1) == 0:
                            continue
                        s1 = s1.pop()
                        s2 = s2.pop()
                        if s1 != s2:
                            if [s1, s2] in automata_final or [s2, s1] in automata_final:
                                eq = 0
                                break
                            else:
                                to.append([s1, s2, letra])
                                eq = -1
                    if eq == 0:
                        automata_final.append([states[i], states[j]])
                    elif eq == -1:
                        s = [states[i], states[j]]
                        s.extend(to)
                        stack[count] = s
                        count += 1
                    else:
                        p1 = pos[states[i]]
                        p2 = pos[states[j]]
                        if p1 != p2:
                            st = equivalente.pop(p2)
                            for s in st:
                                pos[s] = p1
                            equivalente[p1] = equivalente[p1].union(st)
        estado_t = True
        while estado_t and len(stack) > 0:
            estado_t = False
            toremove = set()
            for p, k in stack.items():
                for tr in k[2:]:
                    if [tr[0], tr[1]] in automata_final or [tr[1], tr[0]] in automata_final:
                        stack.pop(p)
                        automata_final.append([k[0], k[1]])
                        estado_t = True
                        break
        for k in stack.values():
            p1 = pos[k[0]]
            p2 = pos[k[1]]
            if p1 != p2:
                st = equivalente.pop(p2)
                for s in st:
                    pos[s] = p1
                equivalente[p1] = equivalente[p1].union(st)
        if len(equivalente) == len(states):
            self.minDFA = self.dfa
        else:
            self.minDFA = self.dfa.automataEstados(
                equivalente, pos)

# Clase para construit un NFA desde expresiones regulares


class NFAfromRegex:
    # Inicializo lo que voy a utilizar
    def __init__(self, regex):
        self.star = '*'
        self.plus = '+'
        self.dot = '.'
        self.openingBracket = '('
        self.closingBracket = ')'
        self.operators = [self.plus, self.dot]
        self.regex = regex
        self.alphabet = [chr(i) for i in range(65, 91)]
        self.alphabet.extend([chr(i) for i in range(97, 123)])
        self.alphabet.extend([chr(i) for i in range(48, 58)])
        self.buildNFA()
    # Obtengo todo lo que necesito del NFA

    def getNFA(self):
        return self.nfa

    def displayNFA(self):
        self.nfa.display()
    # Con lo anterior aqui construyo mi NFA

    def buildNFA(self):
        language = set()
        self.stack = []
        self.automata = []
        previous = "::e::"
        for letra in self.regex:
            if letra in self.alphabet:
                language.add(letra)
                if previous != self.dot and (previous in self.alphabet or previous in [self.closingBracket, self.star]):
                    self.agregarOperadorStack(self.dot)
                self.automata.append(BuildAutomata.simbolos(letra))
            elif letra == self.openingBracket:
                if previous != self.dot and (previous in self.alphabet or previous in [self.closingBracket, self.star]):
                    self.agregarOperadorStack(self.dot)
                self.stack.append(letra)
            elif letra == self.closingBracket:
                if previous in self.operators:
                    raise BaseException(
                        "Error al procesar'%s' despues '%s'" % (letra, previous))
                while(1):
                    if len(self.stack) == 0:
                        raise BaseException(
                            "Error al procesar '%s'. El stack esta vacio" % letra)
                    o = self.stack.pop()
                    if o == self.openingBracket:
                        break
                    elif o in self.operators:
                        self.procesar(o)
            elif letra == self.star:
                if previous in self.operators or previous == self.openingBracket or previous == self.star:
                    raise BaseException(
                        "Error el procesar'%s' despues '%s'" % (letra, previous))
                self.procesar(letra)
            elif letra in self.operators:
                if previous in self.operators or previous == self.openingBracket:
                    raise BaseException(
                        "Error al procesar '%s' despues '%s'" % (letra, previous))
                else:
                    self.agregarOperadorStack(letra)
            else:
                raise BaseException(
                    "El simbolo '%s' no es permitido, LA CADENA NO ES ACEPTADA" % letra)  # verificar si se acepta el lenguaje o no
            previous = letra
        while len(self.stack) != 0:
            op = self.stack.pop()
            self.procesar(op)
        if len(self.automata) > 1:
            print(self.automata)
            raise BaseException("La regexp no se pudo parsear correctamente")
        self.nfa = self.automata.pop()
        self.nfa.language = language
    # Voy agreagando los operadores al stack para ir trabajando con ellos

    def agregarOperadorStack(self, letra):
        while(1):
            if len(self.stack) == 0:
                break
            top = self.stack[len(self.stack)-1]
            if top == self.openingBracket:
                break
            if top == letra or top == self.dot:
                op = self.stack.pop()
                self.procesar(op)
            else:
                break
        self.stack.append(letra)
    # Funcion para procesar el operador

    def procesar(self, operador):
        if len(self.automata) == 0:
            raise BaseException(
                "Error al procesar el operador '%s'. Stack vacio" % operador)
        if operador == self.star:
            a = self.automata.pop()
            self.automata.append(BuildAutomata.simboloEstrella(a))
        elif operador in self.operators:
            if len(self.automata) < 2:
                raise BaseException(
                    "Error al procesar el operador '%s'. operandos incorrectos" % operador)
            a = self.automata.pop()
            b = self.automata.pop()
            if operador == self.plus:
                self.automata.append(BuildAutomata.simboloMas(b, a))
            elif operador == self.dot:
                self.automata.append(BuildAutomata.simboloPunto(b, a))

