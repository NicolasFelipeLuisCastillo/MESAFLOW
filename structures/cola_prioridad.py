
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
        if self.esta_vacia():
            return None
        elemento = heapq.heappop(self._monticulo)
        return elemento[2]

    def primero(self):
        #Mira la más prioritaria SIN sacarla"
        if self.esta_vacia():
            return None
        return self._monticulo[0][2]

    def esta_vacia(self):
        return len(self._monticulo) == 0

    def tamanio(self):
        return len(self._monticulo)

    def _merge_sort(self, lista):
        if len(lista) <= 1:
            return lista
        
        medio = len(lista) // 2
        izq = self._merge_sort(lista[:medio])
        der = self._merge_sort(lista[medio:])
        
        # Mezcla respetando (prioridad, contador)
        resultado = []
        i = j = 0
        while i < len(izq) and j < len(der):
            # Comparamos tuplas: prioridad primero, contador en empate
            if (izq[i][0], izq[i][1]) <= (der[j][0], der[j][1]):
                resultado.append(izq[i])
                i += 1
            else:
                resultado.append(der[j])
                j += 1
        
        resultado.extend(izq[i:])
        resultado.extend(der[j:])
        return resultado

    # Listar usando merge sort.
    def listar(self):
        copia = list(self._monticulo)
        ordenada = self._merge_sort(copia)
        return [elemento[2] for elemento in ordenada]