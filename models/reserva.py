from datetime import datetime, timedelta


class EstadoReserva:
    # Los estados por los que pasa una reserva.

    PENDIENTE = "pendiente"
    EN_CURSO = "en_curso"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"

    VALIDOS = [PENDIENTE, EN_CURSO, COMPLETADA, CANCELADA]


class Reserva:

    #Una reserva: une un cliente, una mesa y un horario.

    #Guardamos el id del cliente y el id de la mesa (no los objetos),
    #así la reserva no se rompe si el cliente o la mesa cambian.


    def __init__(self, id, cliente_id, mesa_id, fecha, hora_inicio,
                 duracion_min=90, estado=EstadoReserva.PENDIENTE):
        self.id = int(id)
        self.cliente_id = int(cliente_id)
        self.mesa_id = int(mesa_id)
        self.fecha = fecha                      # tipo date
        self.hora_inicio = hora_inicio          # tipo time
        self.duracion_min = duracion_min
        self.estado = estado.lower()

    def hora_fin(self):
        #La hora en que termina la reserva.
        inicio = datetime.combine(self.fecha, self.hora_inicio)
        fin = inicio + timedelta(minutes=self.duracion_min)
        return fin.time()

    def minutos_hasta(self):
        #Cuántos minutos faltan desde hoy hasta la reserva.
        ahora = datetime.now()
        inicio = datetime.combine(self.fecha, self.hora_inicio)
        diferencia = inicio - ahora
        return int(diferencia.total_seconds() / 60)

    def solapa_con(self, otra):
        #True si las dos reservas se pisan en el horario.
        if self.fecha != otra.fecha:
            return False

        mi_inicio = datetime.combine(self.fecha, self.hora_inicio)
        mi_fin = datetime.combine(self.fecha, self.hora_fin())
        su_inicio = datetime.combine(otra.fecha, otra.hora_inicio)
        su_fin = datetime.combine(otra.fecha, otra.hora_fin())

        return mi_inicio < su_fin and su_inicio < mi_fin

    def __str__(self):
        return "Reserva #{} - Mesa {} - {} {} - {}".format(
            self.id, self.mesa_id,
            self.fecha, self.hora_inicio.strftime("%H:%M"), self.estado
        )

    # ---- Conversión a/desde diccionario (para el JSON) ----

    def a_dict(self, nombre_cliente, marca_vip):

        #Para el JSON.

        #La reserva guarda el id del cliente, pero la interfaz muestra el
        #nombre. Por eso le pasamos el nombre y si es VIP.

        return {
            "id": str(self.id),
            "cliente": nombre_cliente,
            "vip": "X" if marca_vip else "",
            "mesa": str(self.mesa_id),
            "fecha": self.fecha.isoformat(),
            "hora": self.hora_inicio.strftime("%H:%M"),
            "estado": self.estado.capitalize(),
        }

    @staticmethod
    def desde_dict(datos, id_cliente, id_mesa):

        #Construye una reserva desde el JSON.

        #El JSON guarda el nombre del cliente, pero nosotros necesitamos el id.
        #Eso lo resuelve el gestor, que ya sabe a qué id corresponde cada nombre.

        fecha = datetime.strptime(datos["fecha"], "%Y-%m-%d").date()
        hora = datetime.strptime(datos["hora"], "%H:%M").time()

        return Reserva(
            datos["id"],
            id_cliente,
            id_mesa,
            fecha,
            hora,
            90,
            datos.get("estado", "pendiente"),
        )


class Caminando:
    def __init__(self, id, cliente_id, personas, hora_llegada, mesa_id=None):
        self.id = int(id)
        self.cliente_id = int(cliente_id)
        self.personas = int(personas)
        self.hora_llegada = hora_llegada      # texto "HH:MM"
        self.mesa_id = int(mesa_id) if mesa_id is not None else None

    def __str__(self):
        return "Cliente {} - {} personas - {}".format(
            self.cliente_id, self.personas, self.hora_llegada
        )

    # Conversión a/desde diccionario (para el JSON) 

    def a_dict(self, posicion, nombre_cliente):
        resultado = {
            "pos": str(posicion),
            "id": str(self.id),
            "cliente": nombre_cliente,
            "personas": str(self.personas),
            "hora": self.hora_llegada,
        }
        if self.mesa_id is not None:
            resultado["mesa"] = str(self.mesa_id)
        return resultado

    @staticmethod
    def desde_dict(datos, id_cliente):
        return Caminando(
            datos.get("id", datos.get("pos", 1)),
            id_cliente,
            datos["personas"],
            datos["hora"],
            datos.get("mesa", None),
        )