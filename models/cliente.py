
class Cliente:
    def __init__(self, id, nombre, telefono, es_vip=False):
        self.id = int(id)
        self.nombre = nombre
        self.telefono = telefono
        self.es_vip = bool(es_vip)

    def __str__(self):
        if self.es_vip:
            return "{} (VIP)".format(self.nombre)
        return self.nombre

    # Conversión a/desde diccionario (para el JSON)

    def a_dict(self):
        return {
            "id": str(self.id),
            "nombre": self.nombre,
            "telefono": self.telefono,
            "vip": "X" if self.es_vip else "",
        }

    @staticmethod
    def desde_dict(datos):
        return Cliente(
            datos["id"],
            datos["nombre"],
            datos["telefono"],
            datos.get("vip") == "✓",
        )