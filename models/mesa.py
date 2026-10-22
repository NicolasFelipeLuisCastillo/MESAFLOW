class EstadoMesa:
    #Los 3 estados posibles de una mesa.

    DISPONIBLE = "disponible"
    OCUPADA = "ocupada"
    MANTENIMIENTO = "mantenimiento"

    VALIDOS = [DISPONIBLE, OCUPADA, MANTENIMIENTO]


class UbicacionMesa:
    # Las 3 ubicaciones posibles de una mesa.

    INTERIOR = "interior"
    EXTERIOR = "exterior"
    VENTANA = "ventana"

    VALIDOS = [INTERIOR, EXTERIOR, VENTANA]


class Mesa:
    def __init__(self, id, capacidad, ubicacion, estado=EstadoMesa.DISPONIBLE):
        self.id = int(id)
        self.capacidad = int(capacidad)
        self.ubicacion = ubicacion.lower()
        self.estado = estado.lower()

    def __str__(self):
        return "Mesa {} - {} personas - {} - {}".format(
            self.id, self.capacidad, self.ubicacion, self.estado
        )

    # Conversión a/desde diccionario (para el JSON)

    def a_dict(self):
        # Convierte la mesa a un diccionario para guardarla en el JSON.
        return {
            "id": str(self.id),
            "capacidad": str(self.capacidad),
            "ubicacion": self.ubicacion.capitalize(),
            "estado": self.estado.capitalize(),
        }

    @staticmethod
    def desde_dict(datos):
        # Construye una mesa a partir de un diccionario del JSON.
        return Mesa(
            datos["id"],
            datos["capacidad"],
            datos.get("ubicacion", "interior"),
            datos.get("estado", "disponible"),
        )