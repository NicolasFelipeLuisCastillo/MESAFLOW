from models.cliente import Cliente


class GestorClientes:
    #Guarda y busca los clientes.

    def __init__(self):
        self.clientes = []        # arreglo dinámico
        self.siguiente_id = 1

    def agregar(self, nombre, telefono, es_vip=False):
        #Registra un cliente nuevo y lo devuelve
        cliente = Cliente(self.siguiente_id, nombre.strip(), telefono.strip(), es_vip)
        self.siguiente_id = self.siguiente_id + 1
        self.clientes.append(cliente)
        return cliente

    def obtener(self, id_cliente):
        #Busca un cliente por id. None si no existe
        for cliente in self.clientes:
            if cliente.id == int(id_cliente):
                return cliente
        return None

    def obtener_por_nombre(self, nombre):
        #Busca un cliente por su nombre exacto. None si no existe.
        for cliente in self.clientes:
            if cliente.nombre == nombre:
                return cliente
        return None

    def listar(self):
        return self.clientes

    def eliminar(self, id_cliente):
        #Elimina un cliente. False si no existe.
        cliente = self.obtener(id_cliente)
        if cliente is None:
            return False
        self.clientes.remove(cliente)
        return True

    def buscar_por_nombre(self, texto):
        #Clientes cuyo nombre contenga ese texto (sin importar mayúsculas)
        texto = texto.lower().strip()
        resultado = []
        for cliente in self.clientes:
            if texto in cliente.nombre.lower():
                resultado.append(cliente)
        return resultado

    def buscar_por_telefono(self, telefono):
        #Cliente con ese teléfono exacto. None si no existe
        telefono = telefono.strip()
        for cliente in self.clientes:
            if cliente.telefono == telefono:
                return cliente
        return None

    def es_vip(self, id_cliente):
        #True si el cliente existe y es VIP.
        cliente = self.obtener(id_cliente)
        if cliente is None:
            return False
        return cliente.es_vip

    def total_clientes(self):
        return len(self.clientes)

    def total_vips(self):
        total = 0
        for cliente in self.clientes:
            if cliente.es_vip:
                total = total + 1
        return total

    #ara el JSON 

    def cargar_desde_lista(self, lista_dicts):
        #Carga los clientes desde el JSON
        self.clientes = []
        self.siguiente_id = 1
        for datos in lista_dicts:
            cliente = Cliente.desde_dict(datos)
            self.clientes.append(cliente)
            if cliente.id >= self.siguiente_id:
                self.siguiente_id = cliente.id + 1

    def lista_dicts(self):
        #Devuelve los clientes como lista de diccionarios.
        resultado = []
        for cliente in self.clientes:
            resultado.append(cliente.a_dict())
        return resultado