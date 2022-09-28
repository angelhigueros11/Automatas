from os import popen
import time
import automata as Automata

class Construir_automata:

    @staticmethod
    def init(inp):
        estado = 1
        estado2 = 2
        a = Automata()
        a.setEstadoInicial(estado)
        a.agregarEstados(estado2)
        a.agregarTransiciones(1, 2, inp)
        return a

    @staticmethod
    def mas(a, b):
        [a, m1] = a.automata_numeros(2)
        [b, m2] = b.automata_numeros(m1)
        estado = 1
        estado2 = m2
        p = Automata()
        p.setEstadoInicial(estado)
        p.agregarEstados(estado2)
        p.agregarTransiciones(p.inicial, a.inicial, Automata.epsilon())
        p.agregarTransiciones(p.inicial, b.inicial, Automata.epsilon())
        p.agregarTransiciones(a.final[0], p.final[0], Automata.epsilon())
        p.agregarTransiciones(b.final[0], p.final[0], Automata.epsilon())
        p.agregarTransiciones_dict(a.transitions)
        p.agregarTransiciones_dict(b.transitions)
        return p

    @staticmethod
    def punto(a, b):
        [a, m1] = a.automata_numeros(1)
        [b, m2] = b.automata_numeros(m1)
        estado = 1
        estado2 = m2-1
        p = Automata()
        p.setEstadoInicial(estado)
        p.agregarEstados(estado2)
        p.agregarTransiciones(a.final[0], b.inicial, Automata.epsilon())
        p.agregarTransiciones_dict(a.transitions)
        p.agregarTransiciones_dict(b.transitions)
        return p

    @staticmethod
    def estrella(a):
        [a, m1] = a.automata_numeros(2)
        estado = 1
        estado2 = m1
        s = Automata()
        s.setEstadoInicial(estado)
        s.agregarEstados(estado2)
        s.agregarTransiciones(s.inicial, a.inicial, Automata.epsilon())
        s.agregarTransiciones(s.inicial, s.final[0], Automata.epsilon())
        s.agregarTransiciones(a.final[0], s.final[0], Automata.epsilon())
        s.agregarTransiciones(a.final[0], a.inicial, Automata.epsilon())
        s.agregarTransiciones_dict(a.transitions)
        return s

class Regex_AFN:
    def __init__(self, regex):
        self.estrella = '*'
        self.mas = '+'
        self.punto = '.'
        self.parentesis1 = '('
        self.parentesis2 = ')'
        self.operadores = [self.mas, self.punto]
        self.regex = regex
        self.lenguaje = [chr(i) for i in range(65,91)]
        self.lenguaje.extend([chr(i) for i in range(97,123)])
        self.lenguaje.extend([chr(i) for i in range(48,58)])
        self.construirNFA()

    def getAFN(self):
        return self.nfa

    def displayNFA(self):
        self.nfa.display()

    def construirNFA(self):
        lenguaje = set()
        self.stack = []
        self.automata = []
        previous = "::e::"
        for char in self.regex:
            if char in self.lenguaje:
                lenguaje.add(char)
                if previous != self.punto and (previous in self.lenguaje or previous in [self.parentesis2,self.estrella]):
                    self.addOperatorToStack(self.punto)
                self.automata.append(Construir_automata.init(char))
            elif char  ==  self.parentesis1:
                if previous != self.punto and (previous in self.lenguaje or previous in [self.parentesis2,self.estrella]):
                    self.addOperatorToStack(self.punto)
                self.stack.append(char)
            elif char  ==  self.parentesis2:
                if previous in self.operadores:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                while(1):
                    if len(self.stack) == 0:
                        raise BaseException("Error processing '%s'. Empty stack" % char)
                    o = self.stack.pop()
                    if o == self.parentesis1:
                        break
                    elif o in self.operadores:
                        self.processOperator(o)
            elif char == self.estrella:
                if previous in self.operadores or previous  == self.parentesis1 or previous == self.estrella:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                self.processOperator(char)
            elif char in self.operadores:
                if previous in self.operadores or previous  == self.parentesis1:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                else:
                    self.addOperatorToStack(char)
            else:
                raise BaseException("Symbol '%s' is not allowed" % char)
            previous = char
        while len(self.stack) != 0:
            op = self.stack.pop()
            self.processOperator(op)
        if len(self.automata) > 1:
            print (self.automata)
            raise BaseException("Regex could not be parsed successfully")
        self.nfa = self.automata.pop()
        self.nfa.lenguaje = lenguaje

    def addOperatorToStack(self, char):
        while(1):
            if len(self.stack) == 0:
                break
            top = self.stack[len(self.stack)-1]
            if top == self.parentesis1:
                break
            if top == char or top == self.punto:
                op = self.stack.pop()
                self.processOperator(op)
            else:
                break
        self.stack.append(char)

    def processOperator(self, operator):
        if len(self.automata) == 0:
            raise BaseException("Error processing operator '%s'. Stack is empty" % operator)
        if operator == self.estrella:
            a = self.automata.pop()
            self.automata.append(Construir_automata.estrella(a))
        elif operator in self.operadores:
            if len(self.automata) < 2:
                raise BaseException("Error processing operator '%s'. Inadequate operands" % operator)
            a = self.automata.pop()
            b = self.automata.pop()
            if operator == self.mas:
                self.automata.append(Construir_automata.mas(b,a))
            elif operator == self.punto:
                self.automata.append(Construir_automata.punto(b,a))
