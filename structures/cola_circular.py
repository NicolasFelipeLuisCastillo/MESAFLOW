
    #Cola de tamaño FIJO. Cuando saca un elemento deja un hueco y avanza.
    #Cuando llega al final, vuelve al inicio (gracias al %).

       # Si tengo 4 espacios y el índice está en 3:
            #(3 + 1) % 4 = 0     <- vuelve al inicio

#COSTO:
    #Todas las operaciones son O(1).

#Asignación de mesas para clientes



class ColaCircular:
   #Cola circular de tamaño fijo.

    def __init__(self, capacidad):
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que 0")

        self.capacidad = capacidad
        self.datos = [None] * capacidad
        self.frente = 0
        self.rear = 0
        self.tamanio = 0

    def esta_llena(self):
        return self.tamanio == self.capacidad

    def esta_vacia(self):
        return self.tamanio == 0

    def encolar(self, elemento):
        #Mete un elemento al final. False si está llena.
        if self.esta_llena():
            return False

        self.datos[self.rear] = elemento
        self.rear = (self.rear + 1) % self.capacidad
        self.tamanio = self.tamanio + 1
        return True

    def desencolar(self):
        #Saca el primero. None si está vacía
        if self.esta_vacia():
            return None

        elemento = self.datos[self.frente]
        self.datos[self.frente] = None
        self.frente = (self.frente + 1) % self.capacidad
        self.tamanio = self.tamanio - 1
        return elemento

    def primero(self):
        #Mira el primero SIN sacarlo.
        if self.esta_vacia():
            return None
        return self.datos[self.frente]

    def avanzar(self):

        #EL ROUND-ROBIN.

        #Avanza el frente una posición y devuelve la mesa que quedó ahí.
        #Así las mesas se reparten una por una, sin repetir siempre la misma.

        if self.esta_vacia():
            return None

        self.frente = (self.frente + 1) % self.capacidad
        return self.datos[self.frente]

    def listar(self):
        #Los elementos en orden, empezando por el frente
        resultado = []
        indice = self.frente

        for i in range(self.tamanio):
            elemento = self.datos[indice]
            if elemento is not None:
                resultado.append(elemento)
            indice = (indice + 1) % self.capacidad

        return resultado

    def mostrar(self):
        #Para ver la cola desde la consola
        print("  datos:  ", self.datos)
        print("  frente: ", self.frente)
        print("  rear:   ", self.rear)
        print("  tamaño: ", self.tamanio, "/", self.capacidad)