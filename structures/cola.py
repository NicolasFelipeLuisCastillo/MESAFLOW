
    #El primero que llega es el primero que se atiende.

#COSTO:
    #encolar / desencolar -> O(1)


from collections import deque


class ColaCaminando:
    #Cola normal: entra por atrás, sale por adelante

    def __init__(self):
        self._cola = deque()

    def encolar(self, caminando):
        #Agrega al final de la cola
        self._cola.append(caminando)

    def desencolar(self):
       #Saca el primero de la cola. None si está vacía
        if len(self._cola) == 0:
            return None
        return self._cola.popleft()

    def primero(self):
        #Mira el primero SIN sacarlo
        if len(self._cola) == 0:
            return None
        return self._cola[0]

    def esta_vacia(self):
        return len(self._cola) == 0

    def tamanio(self):
        return len(self._cola)

    def listar(self):
        #Los que están esperando, en orden de llegada
        return list(self._cola)

    def total_personas(self):
        #Suma de cuántas personas están esperando.
        total = 0
        for caminando in self._cola:
            total = total + caminando.personas
        return total