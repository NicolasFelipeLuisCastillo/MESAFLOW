
    #Cola con prioridad -> las reservas pendientes (VIP arriba)
    #Cola FIFO          -> los que llegan caminando (por orden de llegada)
    #Pila LIFO          -> el historial de cancelaciones (el más nuevo arriba)
    #Cola circular      -> para repartir las mesas en round-robin


from datetime import date, time

from models.reserva import Reserva, Caminando, EstadoReserva
from structures.cola_prioridad import ColaPrioridadReservas
from structures.cola import ColaCaminando
from structures.pila import PilaHistorial
from structures.cola_circular import ColaCircular


class GestorReservas:
    #Maneja las reservas usando las 4 estructuras lineales

    def __init__(self, gestor_mesas, gestor_clientes):
        self.gestor_mesas = gestor_mesas
        self.gestor_clientes = gestor_clientes

        # Las 4 estructuras
        self.cola_prioridad = ColaPrioridadReservas()
        self.cola_caminando = ColaCaminando()
        self.pila_historial = PilaHistorial()
        self.cola_mesas = self.armar_cola_circular()

        # Catálogo completo
        self.reservas = []
        self.historial = []          # respaldo del historial (la pila es la que manda)
        self.siguiente_id = 1

    def armar_cola_circular(self):
        #rea la cola circular con todas las mesas del restaurante.
        mesas = self.gestor_mesas.listar()
        capacidad = len(mesas)

        if capacidad == 0:
            capacidad = 1

        cola = ColaCircular(capacidad)
        for mesa in mesas:
            cola.encolar(mesa)
        return cola

    #  RESERVAS


    def crear_reserva(self, id_cliente, id_mesa, fecha, hora, duracion_min=90):
        #Crea una reserva y la mete a la cola con prioridad.
        reserva = Reserva(
            self.siguiente_id, id_cliente, id_mesa, fecha, hora, duracion_min
        )
        self.siguiente_id = self.siguiente_id + 1
        self.reservas.append(reserva)

        # La metemos a la cola con la prioridad correcta
        self.cola_prioridad.encolar(reserva, self.calcular_prioridad(id_cliente))
        return reserva

    def calcular_prioridad(self, id_cliente):
        #VIP = 0 (sale primero), Regular = 1 (sale después).
        if self.gestor_clientes.es_vip(id_cliente):
            return 0
        return 1

    def obtener(self, id_reserva):
        #Busca una reserva por id.
        for reserva in self.reservas:
            if reserva.id == int(id_reserva):
                return reserva
        return None

    def listar_pendientes(self):
        #Las pendientes YA ORDENADAS por la cola con prioridad
        pendientes = self.cola_prioridad.listar()

        # Si algo se modificó fuera de la cola, lo metemos de vuelta
        return [r for r in pendientes if r.estado == EstadoReserva.PENDIENTE]

    def listar_en_curso(self):
        resultado = []
        for reserva in self.reservas:
            if reserva.estado == EstadoReserva.EN_CURSO:
                resultado.append(reserva)
        return resultado

    def total_pendientes(self):
        return self.cola_prioridad.tamanio()

    def confirmar(self, id_reserva):
        #pendiente -> en_curso
        reserva = self.obtener(id_reserva)
        if reserva is None:
            return False
        if reserva.estado != EstadoReserva.PENDIENTE:
            return False
        reserva.estado = EstadoReserva.EN_CURSO
        return True

    def completar(self, id_reserva):
        #en_curso -> completada
        reserva = self.obtener(id_reserva)
        if reserva is None:
            return False
        if reserva.estado != EstadoReserva.EN_CURSO:
            return False
        reserva.estado = EstadoReserva.COMPLETADA
        return True

    def cancelar(self, id_reserva):

        #Cancela una reserva.

        #La saca de la cola y la mete a la PILA de historial

        reserva = self.obtener(id_reserva)

        if reserva is None:
            return False
        if reserva.estado == EstadoReserva.COMPLETADA:
            return False

        reserva.estado = EstadoReserva.CANCELADA
        self.pila_historial.apilar(reserva)
        self.historial.append(reserva)
        return True

    #  LOS QUE LLEGAN CAMINANDO (Cola FIFO)


    def agregar_caminando(self, id_cliente, personas, hora_llegada):
        #Agrega a alguien a la cola de espera, sin reserva.
        self.siguiente_id = self.siguiente_id + 1
        caminando = Caminando(self.siguiente_id, id_cliente, personas, hora_llegada)
        self.cola_caminando.encolar(caminando)
        return caminando

    def atender_caminando(self):
        #Atiende al primero de la fila (FIFO). None si no hay nadie.
        self.ultimo_atendido = self.cola_caminando.desencolar()
        return self.ultimo_atendido

    def ver_caminando(self):
       #Los que están esperando, en orden de llegada.
        return self.cola_caminando.listar()

    def total_caminando(self):
        return self.cola_caminando.tamanio()

    #  ROUND-ROBIN DE MESAS (Cola circular)


    def siguiente_mesa(self):

        #Devuelve la siguiente mesa rotando la cola circular.

        #Si cambiaron las mesas, la reconstruye solito.

        if self.cola_mesas.tamanio != len(self.gestor_mesas.listar()):
            self.cola_mesas = self.armar_cola_circular()

        return self.cola_mesas.avanzar()

    def ver_orden_mesas(self):
        return self.cola_mesas.listar()

    #  HISTORIAL (Pila LIFO)


    def ver_historial(self):
        #Las cancelaciones, la más reciente primero.
        return self.pila_historial.listar()

    def total_cancelaciones(self):
        return self.pila_historial.tamanio()

    #  CHEQUEO DE DISPONIBILIDAD


    def mesa_esta_libre(self, id_mesa, fecha, hora, duracion_min=90):
        #True si esa mesa está libre en ese horario.
        id_mesa = int(id_mesa)

        # Armamos una reserva de prueba solo para comparar horarios
        prueba = Reserva(-1, -1, id_mesa, fecha, hora, duracion_min, "pendiente")

        for reserva in self.reservas:
            if reserva.mesa_id != id_mesa:
                continue
            if reserva.estado == EstadoReserva.CANCELADA:
                continue
            if reserva.estado == EstadoReserva.COMPLETADA:
                continue
            if prueba.solapa_con(reserva):
                return False

        return True


    #  PARA EL JSON


    def cargar_desde_listas(self, reservas_dicts, caminando_dicts, historial_dicts):
        #Carga todo desde el JSON.
        self.reservas = []
        self.historial = []
        self.siguiente_id = 1
        self.cola_prioridad = ColaPrioridadReservas()
        self.cola_caminando = ColaCaminando()
        self.pila_historial = PilaHistorial()

        # Primero los clientes y las mesas, porque las reservas los necesitan
        for datos in reservas_dicts:
            cliente = self.gestor_clientes.obtener_por_nombre(datos["cliente"])
            if cliente is None:
                continue   # el cliente ya no existe, saltamos la reserva

            mesa = self.gestor_mesas.obtener(datos["mesa"])
            if mesa is None:
                mesa_id = datos["mesa"]
            else:
                mesa_id = mesa.id

            reserva = Reserva.desde_dict(datos, cliente.id, mesa_id)
            self.reservas.append(reserva)

            if reserva.id >= self.siguiente_id:
                self.siguiente_id = reserva.id + 1

            # Solo las pendientes van a la cola con prioridad
            if reserva.estado == EstadoReserva.PENDIENTE:
                self.cola_prioridad.encolar(reserva, self.calcular_prioridad(cliente.id))

        for datos in caminando_dicts:
            cliente = self.gestor_clientes.obtener_por_nombre(datos["cliente"])
            if cliente is None:
                continue

            self.siguiente_id = self.siguiente_id + 1
            caminando = Caminando(
                self.siguiente_id, cliente.id,
                datos["personas"], datos["hora"]
            )
            self.cola_caminando.encolar(caminando)

        # El historial se carga en orden inverso, porque la pila
        # muestra el último arriba. El JSON guarda el primero arriba.
        for datos in reversed(historial_dicts):
            cliente = self.gestor_clientes.obtener_por_nombre(datos["cliente"])
            cliente_id = cliente.id if cliente is not None else -1

            from datetime import datetime
            fecha = datetime.strptime(datos["fecha"], "%Y-%m-%d").date()
            hora = datetime.strptime(datos["hora"], "%H:%M").time()

            reserva = Reserva(
                datos["id"], cliente_id, datos["mesa"],
                fecha, hora, 90, "cancelada"
            )
            self.pila_historial.apilar(reserva)
            self.historial.append(reserva)

        self.cola_mesas = self.armar_cola_circular()