
from automatas import *
import sys

class AFN_AFD:
    def __init__(self, afn):
        self.generar_afd(afn)
        self.minimizar()

    def getAFN(self):
        return self.afd

    def getAFDminimizado(self):
        return self.AFDmin

    def aceptarCadena(self, string):
        string = self.afd.inicial
        for ch in string:
            if ch==":e:":
                continue
            st = list(self.afd.obtenerTransiciones(string, ch))
            if len(st) == 0:
                return False
            string = st[0]
        if string in self.afd.final:
            return True
        return False




    def generarAFDMinimizado(self):
        self.AFDmin.guardar()

    def constrirAFD(self, afn):
        estados = dict()
        eclose = dict()
        count = 1
        state1 = afn.getEClose(afn.inicial)
        eclose[afn.inicial] = state1
        afd = Automata(afn.lenguaje)
        afd.setEstadoInicial(count)
        states = [[state1, count]]
        estados[count] = state1
        count +=  1
        while len(states) != 0:
            [state, fromindex] = states.pop()
            for char in afd.lenguaje:
                trstates = afn.obtenerTransiciones(state, char)
                for s in list(trstates)[:]:
                    if s not in eclose:
                        eclose[s] = afn.getEClose(s)
                    trstates = trstates.union(eclose[s])
                if len(trstates) != 0:
                    if trstates not in estados.values():
                        states.append([trstates, count])
                        estados[count] = trstates
                        toindex = count
                        count +=  1
                    else:
                        toindex = [k for k, v in estados.iteritems() if v  ==  trstates][0]
                    afd.agregarTransiciones(fromindex, toindex, char)
        for value, state in estados.iteritems():
            if afn.final[0] in state:
                afd.agregarEstados(value)
        self.afd = afd


    def minimise(self):
        states = list(self.afd.states)
        n = len(states)
        v = dict()
        count = 1
        d = []
        equivalente = dict(zip(range(len(states)), [{s} for s in states]))
        pos = dict(zip(states,range(len(states))))
        for i in range(n-1):
            for j in range(i+1, n):
                if not ([states[i], states[j]] in d or [states[j], states[i]] in d):
                    eq = 1
                    estados_agregar = []
                    for char in self.afd.lenguaje:
                        s1 = self.afd.obtenerTransiciones(states[i], char)
                        s2 = self.afd.obtenerTransiciones(states[j], char)
                        if len(s1) != len(s2):
                            eq = 0
                            break
                        if len(s1) > 1:
                            raise BaseException("[!] Error")
                        elif len(s1) == 0:
                            continue
                        s1 = s1.pop()
                        s2 = s2.pop()
                        if s1 != s2:
                            if [s1, s2] in d or [s2, s1] in d:
                                eq = 0
                                break
                            else:
                                estados_agregar.append([s1, s2, char])
                                eq = -1
                    if eq == 0:
                        d.append([states[i], states[j]])
                    elif eq == -1:
                        s = [states[i], states[j]]
                        s.extend(estados_agregar)
                        v[count] = s
                        count += 1
                    else:
                        p1 = pos[states[i]]
                        p2 = pos[states[j]]
                        if p1 != p2:
                            st = equivalente.pop(p2)
                            for s in st:
                                pos[s] = p1
                            equivalente[p1] = equivalente[p1].union(st)
        buscar = True
        while buscar and len(v) > 0:
            buscar = False
            quitar = set()
            for p, pp in v.items():
                for tr in pp[2:]:
                    if [tr[0], tr[1]] in d or [tr[1], tr[0]] in d:
                        v.pop(p)
                        d.append([pp[0], pp[1]])
                        buscar = True
                        break
        for pp in v.values():
            p1 = pos[pp[0]]
            p2 = pos[pp[1]]
            if p1 != p2:
                st = equivalente.pop(p2)
                for s in st:
                    pos[s] = p1
                equivalente[p1] = equivalente[p1].union(st)
        if len(equivalente) == len(states):
            self.AFDmin = self.afd
        else:
            self.AFDmin = self.afd.automata_estados(equivalente, pos)
        
    def mostrarAFD(self):
        self.afd.guardar()