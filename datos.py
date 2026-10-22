
#1. GUARDAR y CARGAR el JSON (usando los servicios, no listas sueltas)
#2. CONVERTIR los objetos del modelo en diccionarios que la interfaz
#puede mostrar en las tablas

#Así la interfaz nunca toca las estructuras directamente:
#siempre le pide los datos al gestor y los convierte con las
#funciones de acá.


import json
import os

ARCHIVO = "datos_mesaflow.json"


#  1. GUARDAR Y CARGAR
# =====================================================
def cargar_sistema(gestor_mesas, gestor_clientes, gestor_reservas):

    #Lee el JSON (si existe) y llena los 3 servicios con esa información.

    #El orden importa:
      #1. Primero las mesas
      #2. Después los clientes
      #3. Al final las reservas, porque necesitan de mesas y clientes


    if not os.path.exists(ARCHIVO):
        return False   # no hay archivo, no se carga nada

    archivo = open(ARCHIVO, "r", encoding="utf-8")
    datos = json.load(archivo)
    archivo.close()

    gestor_mesas.cargar_desde_lista(datos.get("mesas", []))
    gestor_clientes.cargar_desde_lista(datos.get("clientes", []))
    gestor_reservas.cargar_desde_listas(
        datos.get("reservas", []),
        datos.get("caminando", []),
        datos.get("historial", []),
    )
    return True


def guardar_sistema(gestor_mesas, gestor_clientes, gestor_reservas):
    #Arma el diccionario con todo el estado y lo escribe en el JSON.

    datos = {
        "mesas": gestor_mesas.lista_dicts(),
        "clientes": gestor_clientes.lista_dicts(),
        "reservas": reservas_a_dicts(gestor_reservas, gestor_clientes),
        "caminando": caminando_a_dicts(gestor_reservas, gestor_clientes),
        "historial": historial_a_dicts(gestor_reservas, gestor_clientes),
    }

    archivo = open(ARCHIVO, "w", encoding="utf-8")
    json.dump(datos, archivo, indent=4, ensure_ascii=False)
    archivo.close()


#  2. CONVERTIR LOS OBJETOS EN DICCIONARIOS PARA LAS TABLAS

def mesas_para_tabla(gestor_mesas):
    #Lista de mesas en el formato que la tabla espera.
    resultado = []
    for mesa in gestor_mesas.listar():
        resultado.append(mesa.a_dict())
    return resultado


def clientes_para_tabla(gestor_clientes):
    #Lista de clientes en el formato que la tabla espera.
    resultado = []
    for cliente in gestor_clientes.listar():
        resultado.append(cliente.a_dict())
    return resultado


def reservas_para_tabla(gestor_reservas, gestor_clientes):

    #Las reservas PENDIENTES, ya ordenadas por la cola con prioridad.

    #El orden lo pone la estructura (ColaPrioridadReservas),
    #no un sorted() aquí adentro.

    resultado = []

    for reserva in gestor_reservas.listar_pendientes():
        cliente = gestor_clientes.obtener(reserva.cliente_id)
        if cliente is None:
            continue

        resultado.append(reserva.a_dict(cliente.nombre, cliente.es_vip))

    return resultado


def reservas_en_curso_para_tabla(gestor_reservas, gestor_clientes):
   #Las reservas que ya están confirmadas (cliente sentado)
    resultado = []

    for reserva in gestor_reservas.listar_en_curso():
        cliente = gestor_clientes.obtener(reserva.cliente_id)
        if cliente is None:
            continue

        resultado.append(reserva.a_dict(cliente.nombre, cliente.es_vip))

    return resultado


def caminando_para_tabla(gestor_reservas, gestor_clientes):

    #Los que esperan, EN ORDEN DE LLEGADA (FIFO).

    #El orden lo da la ColaCaminando, no un sort().

    resultado = []
    posicion = 1

    for caminando in gestor_reservas.ver_caminando():
        cliente = gestor_clientes.obtener(caminando.cliente_id)
        nombre = cliente.nombre if cliente is not None else "Desconocido"

        resultado.append(caminando.a_dict(posicion, nombre))
        posicion = posicion + 1

    return resultado


def historial_para_tabla(gestor_reservas, gestor_clientes):

    #Las cancelaciones, LA MÁS RECIENTE ARRIBA (LIFO).

    #El orden lo da la PilaHistorial, no un [::-1] manual.

    resultado = []

    for reserva in gestor_reservas.ver_historial():
        cliente = gestor_clientes.obtener(reserva.cliente_id)
        nombre = cliente.nombre if cliente is not None else "Desconocido"

        hora = reserva.hora_inicio.strftime("%H:%M")
        fecha = reserva.fecha.isoformat()

        resultado.append({
            "id": str(reserva.id),
            "cliente": nombre,
            "mesa": str(reserva.mesa_id),
            "fecha": fecha,
            "hora": hora,
            "tiempo": "Hace un momento",
        })

    return resultado


#Funciones que usan los conversores, para el guardado

def reservas_a_dicts(gestor_reservas, gestor_clientes):
    resultado = []
    for reserva in gestor_reservas.reservas:
        cliente = gestor_clientes.obtener(reserva.cliente_id)
        nombre = cliente.nombre if cliente is not None else "Desconocido"
        vip = cliente.es_vip if cliente is not None else False
        resultado.append(reserva.a_dict(nombre, vip))
    return resultado


def caminando_a_dicts(gestor_reservas, gestor_clientes):
    resultado = []
    posicion = 1
    for caminando in gestor_reservas.ver_caminando():
        cliente = gestor_clientes.obtener(caminando.cliente_id)
        nombre = cliente.nombre if cliente is not None else "Desconocido"
        resultado.append(caminando.a_dict(posicion, nombre))
        posicion = posicion + 1
    return resultado


def historial_a_dicts(gestor_reservas, gestor_clientes):
    resultado = []
    # Guardamos el más antiguo primero, porque al cargar se vuelve a voltear
    for reserva in gestor_reservas.historial:
        cliente = gestor_clientes.obtener(reserva.cliente_id)
        nombre = cliente.nombre if cliente is not None else "Desconocido"
        resultado.append({
            "id": str(reserva.id),
            "cliente": nombre,
            "mesa": str(reserva.mesa_id),
            "fecha": reserva.fecha.isoformat(),
            "hora": reserva.hora_inicio.strftime("%H:%M"),
            "tiempo": "Hace un momento",
        })
    return resultado