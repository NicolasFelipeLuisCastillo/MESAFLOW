
    #La última cancelación que entró es la primera que sale.
    #(LIFO = Último que entra, primero que sale)

#COSTO:
    #apilar / desapilar -> O(1)


from datetime import datetime


class PilaHistorial:
    #Pila: entra y sale siempre por el mismo lado.

    def __init__(self):
        self._pila = []

    def apilar(self, elemento):
        #Pone algo en la cima de la pila
        self._pila.append(elemento)

    def desapilar(self):
        #Saca la cima. None si está vacía
        if self.esta_vacia():
            return None
        return self._pila.pop()

    def cima(self):
        #Mira la cima SIN sacarla.
        if self.esta_vacia():
            return None
        return self._pila[-1]

    def esta_vacia(self):
        return len(self._pila) == 0

    def tamanio(self):
        return len(self._pila)

    def listar(self):
        #Los elementos con el más reciente primero
        return self._pila[::-1]