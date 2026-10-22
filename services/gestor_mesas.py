from models.mesa import Mesa, EstadoMesa, UbicacionMesa


class GestorMesas:
    #Guarda y busca las mesas.

    def __init__(self):
        self.mesas = []          # arreglo dinámico
        self.siguiente_id = 1

    def agregar(self, capacidad, ubicacion):
        #Registra una mesa nueva y la devuelve. None si los datos no sirven.
        if str(capacidad).isdigit() is False:
            return None
        if int(capacidad) < 1 or int(capacidad) > 20:
            return None

        ubicacion = str(ubicacion).lower()
        if ubicacion not in UbicacionMesa.VALIDOS:
            return None

        mesa = Mesa(self.siguiente_id, int(capacidad), ubicacion)
        self.siguiente_id = self.siguiente_id + 1
        self.mesas.append(mesa)
        return mesa

    def obtener(self, id_mesa):
        #Busca una mesa por id. None si no existe.
        for mesa in self.mesas:
            if mesa.id == int(id_mesa):
                return mesa
        return None

    def listar(self):
        return self.mesas

    def eliminar(self, id_mesa):
        #Elimina una mesa. False si no existe o está ocupada.
        mesa = self.obtener(id_mesa)

        if mesa is None:
            return False
        if mesa.estado == EstadoMesa.OCUPADA:
            return False

        self.mesas.remove(mesa)
        return True

    def cambiar_estado(self, id_mesa, estado_nuevo):
        #Cambia el estado de una mesa. False si no existe o el estado no sirve.
        mesa = self.obtener(id_mesa)

        if mesa is None:
            return False

        estado_nuevo = str(estado_nuevo).lower()
        if estado_nuevo not in EstadoMesa.VALIDOS:
            return False

        mesa.estado = estado_nuevo
        return True

    def disponibles(self):
        resultado = []
        for mesa in self.mesas:
            if mesa.estado == EstadoMesa.DISPONIBLE:
                resultado.append(mesa)
        return resultado

    def con_capacidad_minima(self, personas):
        resultado = []
        for mesa in self.mesas:
            if mesa.capacidad >= personas:
                resultado.append(mesa)
        return resultado

    def total_mesas(self):
        return len(self.mesas)

    # Para el JSON

    def cargar_desde_lista(self, lista_dicts):
       #Carga las mesas desde el JSON
        self.mesas = []
        self.siguiente_id = 1
        for datos in lista_dicts:
            mesa = Mesa.desde_dict(datos)
            self.mesas.append(mesa)
            if mesa.id >= self.siguiente_id:
                self.siguiente_id = mesa.id + 1

    def lista_dicts(self):
        #Devuelve las mesas como lista de diccionarios
        resultado = []
        for mesa in self.mesas:
            resultado.append(mesa.a_dict())
        return resultado