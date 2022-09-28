from os import popen
import time

class Automata:
    def __init__(self, lenguaje = set(['0', '1'])):
        self.estados = set()
        self.inicial = None
        self.final = []
        self.lenguaje = lenguaje
        self.transiciones = dict()


    @staticmethod
    def epsilon():
        return ":e:"

    def setEstadoInicial(self, state):
        self.inicial = state
        self.estados.add(state)

    def agregarEstados(self, state):
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.final:
                self.final.append(s)

    def agregarTransiciones(self, desde, hacia, regex):
        if isinstance(regex, str):
            regex = set([regex])
        self.estados.add(desde)
        self.estados.add(hacia)
        if desde in self.transiciones:
            if hacia in self.transiciones[desde]:
                self.transiciones[desde][hacia] = self.transiciones[desde][hacia].union(regex)
            else:
                self.transiciones[desde][hacia] = regex
        else:
            self.transiciones[desde] = {hacia : regex}

    def agregarTransiciones_dict(self, transiciones):
        for desde, destinos in transiciones.items():
            for state in destinos:
                self.agregarTransiciones(desde, state, destinos[state])

    def obtenerTransiciones(self, state, key):
        if isinstance(state, int):
            state = [state]
        estado_transiciones = set()
        for st in state:
            if st in self.transiciones:
                for tns in self.transiciones[st]:
                    if key in self.transiciones[st][tns]:
                        estado_transiciones.add(tns)
        return estado_transiciones

    def getEstadoFinal(self, estado_encontrar):
        allstates = set()
        states = set([estado_encontrar])
        while len(states) != 0:
            state = states.pop()
            allstates.add(state)
            if state in self.transiciones:
                for tns in self.transiciones[state]:
                    if Automata.epsilon() in self.transiciones[state][tns] and tns not in allstates:
                        states.add(tns)
        return allstates

    def guardar(self):
        print ("ESTADOS:", self.estados)
        print ("SIMBOLOS", self.inicial)
        print ("TRANSICIONES:")
        for desde, destinos in self.transiciones.items():
            for state in destinos:
                for i in destinos[state]:
                    print ("  ",desde, "->", state, "on '"+i+"'" )
            # print

    def getPrintText(self):
        text = "lenguaje: {" + ", ".join(self.lenguaje) + "}\n"
        text += "states: {" + ", ".join(map(str,self.estados)) + "}\n"
        text += "start state: " + str(self.inicial) + "\n"
        text += "final states: {" + ", ".join(map(str,self.final)) + "}\n"
        text += "transitions:\n"
        linecount = 5
        for desde, destinos in self.transiciones.items():
            for state in destinos:
                for char in destinos[state]:
                    text += "    " + str(desde) + " -> " + str(state) + " on '" + char + "'\n"
                    linecount +=1
        return [text, linecount]

    def automata_numeros(self, numero_init):
        transiciones = {}
        for i in list(self.estados):
            transiciones[i] = numero_init
            numero_init += 1
        rebuild = Automata(self.lenguaje)
        rebuild.setEstadoInicial(transiciones[self.inicial])
        rebuild.agregarEstados(transiciones[self.final[0]])
        for desde, destinos in self.transiciones.items():
            for state in destinos:
                rebuild.agregarTransiciones(transiciones[desde], transiciones[state], destinos[state])
        return [rebuild, numero_init]

    def automata_estados(self, equivalent, pos):
        rebuild = Automata(self.lenguaje)
        for desde, destinos in self.transiciones.items():
            for state in destinos:
                rebuild.agregarTransiciones(pos[desde], pos[state], destinos[state])
        rebuild.setEstadoInicial(pos[self.inicial])
        for s in self.final:
            rebuild.agregarEstados(pos[s])
        return rebuild


