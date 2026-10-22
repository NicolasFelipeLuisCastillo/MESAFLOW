
    #VIP      -> prioridad 0  (sale primero)
    #Regular -> prioridad 1  (sale después)
    #Y dentro de cada grupo sale primero el que se encoló antes.

#COSTO:
    #encolar / desencolar -> O(log n)
    #primero             -> O(1)

import heapq


class ColaPrioridadReservas:
    #Cola donde siempre sale primero lo más prioritario

    def __init__(self):
        # Cada elemento es una tupla: (prioridad, numero, reserva)
        # El "numero" es un contador para desempatar.
        self._monticulo = []
        self._contador = 0

    def encolar(self, reserva, prioridad):
        #Mete una reserva con su prioridad (0 = VIP, 1 = regular)
        self._contador = self._contador + 1
        heapq.heappush(self._monticulo, (prioridad, self._contador, reserva))

    def desencolar(self):
        #Saca la más prioritaria. None si está vacía
        if len(self._monticulo) == 0:
            return None
        elemento = heapq.heappop(self._monticulo)
        return elemento[2]

    def primero(self):
        #Mira la más prioritaria SIN sacarla"
        if len(self._monticulo) == 0:
            return None
        return self._monticulo[0][2]

    def esta_vacia(self):
        return len(self._monticulo) == 0

    def tamanio(self):
        return len(self._monticulo)

    def listar(self):
        #Todas las reservas en orden de prioridad (sin sacarlas).
        copia = list(self._monticulo)
        copia.sort()
        resultado = []
        for elemento in copia:
            resultado.append(elemento[2])
        return resultado