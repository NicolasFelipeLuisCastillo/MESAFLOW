![1792636944496](images/README/1792636944496.png)

# MesaFlow

Sistema de gestión de reservas para restaurantes, desarrollado en Python con interfaz gráfica. Forma parte de la primera fase del curso de Estructuras de Datos, en la que el objetivo es aplicar estructuras lineales para resolver un problema real de negocio.

El sistema resuelve un conflicto concreto: en un restaurante hay tres flujos que compiten entre sí (reservas anticipadas, clientes que llegan sin reserva y cancelaciones) y, sin una herramienta que los ordene, la atención se resuelve a criterio del personal. MesaFlow los organiza de forma automática.

---

## Requisitos

- Python 3.9 o superior
- Las siguientes bibliotecas:

```
customtkinter>=5.2.0
pillow>=9.0.0
pytest>=7.4.0
```

Para instalarlas:

```bash
pip install -r requirements.txt
```

---

## Cómo ejecutarlo

El programa se lanza desde la raíz de la carpeta `reservas`, porque los módulos usan imports absolutos que requieren esa ubicación.

```bash
cd reservas
python main.py
```

Al iniciar, si no existe un archivo de datos previo, el sistema carga cinco mesas y tres clientes de ejemplo para poder probarlo sin tener que registrarlos a mano.

Los datos se guardan automaticamente en `datos_mesaflow.json`, en la misma carpeta. Al cerrar y volver a abrir la aplicación, toda la información se recupera.

Para ejecutar las pruebas:

```bash
python run_tests.py                      # pruebas de las estructuras
python test_integracion_gui.py           # prueba del flujo completo
python test_sin_mocks.py                 # verifica que la interfaz use los servicios
```

---

## Manual de usuario

La aplicación tiene una sola ventana con un menú lateral de seis secciones. Cada una tiene un comportamiento distinto. A continuación se explica qué hace y cómo se usa.

### Mesas

Permite registrar las mesas del restaurante con su capacidad y su ubicación (interior, exterior o ventana).

Para agregar una mesa se escribe la cantidad de personas en el campo Capacidad, se elige la ubicación del desplegable y se presiona el botón Agregar mesa. La capacidad debe ser un número entre 1 y 20; cualquier otro valor es rechazado con un mensaje de error.

La tabla muestra todas las mesas con su identificador, capacidad, ubicación y estado actual. Para eliminar una mesa hay que seleccionarla en la tabla y presionar el botón rojo. El sistema pide confirmación antes de eliminarla, y se niega a borrar una mesa que esté en estado ocupada.

### Clientes

Permite registrar a los clientes del restaurante con su nombre, teléfono y una indicación de si son VIP o no.

El campo Telefono acepta únicamente dígitos, guiones y espacios, con una longitud entre 7 y 15 caracteres. Cualquier otro formato es rechazado.

La tabla muestra los clientes registrados, marcando con un asterisco a los que son VIP. El campo de búsqueda filtra la tabla por nombre mientras se escribe. Para eliminar un cliente se lo selecciona en la tabla y se presiona el botón correspondiente; el sistema pide confirmación.

La marca de VIP tiene un efecto directo en el sistema: los clientes VIP reciben prioridad en la cola de reservas, como se explica más adelante.

### Reservas

Es la pantalla principal. Aquí se crean las reservas y se controla el orden en que se atienden.

Para crear una reserva se elige el cliente del desplegable, se escribe la hora en formato HH:MM y se presiona Crear reserva. La mesa no se elige manualmente: el sistema la asigna automáticamente mediante un mecanismo de reparto circular, y el número asignado aparece en el campo de mesa una vez confirmada la operación.

Las reservas se muestran ordenadas por prioridad de atención. Los clientes VIP aparecen primero, independientemente de la hora de su reserva. Entre los clientes de la misma categoría, aparece primero el que reservó antes.

El borde del formulario se vuelve morado cuando el cliente seleccionado en el desplegable es VIP, como recordatorio visual de la prioridad.

El sistema valida que la hora esté dentro del horario de atención del restaurante, entre las 12:00 y las 23:00. También verifica que la mesa asignada no tenga ya una reserva que se superponga en el horario.

Con el botón Confirmar la reserva pasa del estado Pendiente a En curso, lo que indica que el cliente ya está sentado. Con el botón Cancelar Reserva la reserva se elimina de la lista y queda registrada en el historial.

### Caminando

Gestiona los clientes que llegan al local sin reserva previa.

Para agregar a alguien a la fila se elige el cliente, se indica la cantidad de personas y la hora de llegada, y se presiona Agregar a la cola.

La tabla muestra la fila en orden de llegada, con una columna de posición numerada. El botón Atender siguiente retira a la primera persona de la fila y muestra un mensaje confirmando a quién se atendió.

### Historial

Muestra las reservas que fueron canceladas, de la más reciente a la más antigua.

Cuando el historial está vacío, la pantalla muestra un mensaje en lugar de la tabla. A medida que se acumulan cancelaciones, la más reciente siempre aparece en la primera fila, de modo que el usuario puede consultar de inmediato lo que acaba de ocurrir.

---

## Las estructuras de datos y por que se eligieron

El proyecto utiliza cuatro estructuras lineales. La elección de cada una no fue arbitraria: en todos los casos se partió de observar cuál es el comportamiento real que el sistema debe modelar, y luego se buscó la estructura que lo representa con la menor complejidad.

### Cola con prioridad

Se utiliza en el archivo `structures/cola_prioridad.py` y administra las reservas pendientes de atención.

La razón para usarla es que el orden de atención en un restaurante no es estrictamente cronológico. Un cliente VIP que reservó para las 21:00 debe ser atendido antes que un cliente regular que reservó para las 18:00. Si se usara una cola común, cuyo criterio es el orden de llegada, esa reserva quedaría última. La cola con prioridad resuelve exactamente este caso: el criterio de ordenamiento no es cuándo llegó el elemento, sino qué tan prioritario es.

La implementación se apoya en el módulo `heapq` de la biblioteca estándar, que implementa un montículo binario. Cada elemento se guarda como una tupla de tres valores: la prioridad, un contador incremental y la reserva. El orden entre elementos se resuelve comparando primero la prioridad y, en caso de empate, el contador.

La prioridad se calcula en el servicio de reservas a partir de una consulta al gestor de clientes: si el cliente es VIP se le asigna prioridad 0, y si es regular se le asigna prioridad 1. Como el montículo ordena de menor a mayor, la prioridad 0 siempre sale antes que la 1.

El contador cumple una función específica: hacer que la estructura sea estable. Sin él, dos reservas con la misma prioridad podrían salir en un orden arbitrario. Con el contador, dentro de cada categoría de prioridad se mantiene el orden real de llegada, porque el contador refleja el orden en que fueron insertadas.

Las operaciones de encolar y desencolar tienen una complejidad de O(log n), mientras que consultar el primer elemento es O(1). Es un costo ligeramente mayor que el de una cola común, que trabaja en O(1), pero a cambio se obtiene el control sobre el criterio de ordenamiento. Para el volumen de datos de un restaurante, ese costo es irrelevante.

### Cola FIFO

Se utiliza en el archivo `structures/cola.py` y administra la fila de clientes que llegan sin reserva.

El comportamiento que hay que modelar es el de una fila de espera común, donde el orden de llegada es vinculante: el primero que llegó debe ser el primero en ser atendido. Este es el caso más simple de los cuatro y también el más fácil de justificar, porque una cola común es exactamente la representación de una fila.

La implementación utiliza `collections.deque` en lugar de una lista común. La razón es técnica pero relevante: en una lista de Python, eliminar el primer elemento obliga al intérprete a desplazar todos los elementos restantes una posición hacia adelante, lo que implica una complejidad de O(n). Con `deque`, el acceso y la eliminación por el frente tienen complejidad O(1). La diferencia es imperceptible con diez personas en la fila, pero con decenas de miles la diferencia sería de varios órdenes de magnitud.

### Pila LIFO

Se utiliza en el archivo `structures/pila.py` y administra el historial de cancelaciones.

El comportamiento que se necesita es el inverso al de la cola. Cuando un cliente cancela, lo que el personal quiere consultar primero es la cancelación que ocurrió hace un momento, no la más antigua. En una cola, el elemento más antiguo quedaría primero. En una pila, el elemento más reciente queda siempre en la cima y es el primero al que se accede.

Esta es la razón principal por la que se eligió una pila en lugar de una cola, y es un detalle pequeño pero que define la utilidad real de la pantalla de historial. Si se usara una cola, el usuario tendría que desplazarse hasta el final para ver lo que acaba de pasar, lo que es exactamente lo contrario de lo que se busca en una pantalla de auditoría.

La implementación utiliza una lista común de Python, porque las listas ya tienen el comportamiento de pila de forma nativa: el método `append` agrega al final y el método `pop` elimina el último. Ambas operaciones tienen complejidad O(1). El método `listar` devuelve una copia de la pila en orden inverso, de modo que la más reciente aparezca primero, sin modificar el contenido original.

### Cola circular

Se utiliza en el archivo `structures/cola_circular.py` y administra el reparto de las mesas entre los clientes.

El problema que resuelve es la asignación de mesas. Si se usara el criterio habitual de buscar siempre la primera mesa disponible, el primer cliente de cada franja horaria recibiría la mesa número uno, y el último recibiría la que siempre queda más desfavorecida. La cola circular reparte las mesas de manera secuencial y, cuando llega al final, vuelve al principio, dando un trato equitativo a todos.

Esta es la única de las cuatro estructuras que está implementada completamente a mano, sin apoyarse en ninguna librería de Python, porque el enunciado del proyecto la requiere de esa forma.

La estructura utiliza una lista de tamaño fijo, más tres variables: `frente`, que indica la posición del primer elemento, `rear`, que indica dónde se insertará el próximo, y `tamanio`, que indica cuántos elementos hay. El mecanismo que permite que el índice se reinicie al llegar al final es el operador módulo, escrito como signo porcentaje. Cuando el índice alcanza el valor de la capacidad, la operación módulo devuelve cero y el índice vuelve al principio.

Todas las operaciones tienen complejidad O(1). No hay búsqueda ni desplazamiento de elementos, ya que el acceso se hace directamente a una posición conocida de la lista. El detalle relevante para la corrección es que, si la cantidad de mesas cambia durante la ejecución, la cola queda desactualizada. Por ese motivo el servicio de reservas compara el tamaño de la cola con la cantidad de mesas registradas y la reconstruye automáticamente cuando no coinciden.

---

## Arquitectura del proyecto

El código está organizado en cuatro capas. Cada capa depende de la que tiene debajo y nunca accede directamente a una que está por encima. Esta separación es lo que permite que la interfaz gráfica se desarrolle de forma independiente de la implementación de las estructuras.

La capa de modelos (`models/`) contiene las clases `Mesa`, `Cliente`, `Reserva` y `Caminando`. Solo almacenan información y no conocen nada sobre la interfaz ni sobre las estructuras.

La capa de estructuras (`structures/`) contiene las cuatro estructuras lineales. Aquí viven los algoritmos, y estas clases no saben qué es una mesa ni qué es una reserva: reciben objetos genéricos y los ordenan.

La capa de servicios (`services/`) contiene los tres gestores. El `GestorReservas` es el que utiliza las cuatro estructuras y es, en términos prácticos, el lugar donde vive la lógica de negocio.

La capa de interfaz está formada por `main.py` y `vistas.py`. Las cinco pantallas solo dibujan elementos y capturan eventos de clic. Cuando necesitan operar datos, llaman a un método del servicio correspondiente.

Entre la interfaz y los modelos existe el archivo `datos.py`, que cumple dos funciones. La primera es convertir los objetos del modelo en diccionarios que las tablas de la interfaz puedan mostrar, porque los servicios devuelven objetos y las tablas necesitan filas. La segunda es leer y escribir el archivo JSON de persistencia.

Esta separación tiene una consecuencia práctica que conviene destacar. En una versión anterior del proyecto, la interfaz funcionaba correctamente pero operaba sobre listas de Python comunes y reordenaba los datos de forma manual. Las cuatro estructuras existían en el proyecto pero no eran utilizadas por la aplicación. La reorganización consistió en hacer que cada pantalla solicitara los datos a los servicios, y que los servicios usaran las estructuras. Para evitar una regresión de ese tipo, se escribió una prueba que lee el código fuente de las vistas y falla si detecta el uso de ordenamientos manuales o de listas sueltas.

---

## Estructura de carpetas

```
reservas/
├── main.py                  Ventana principal y creación de los servicios
├── datos.py                 Persistencia JSON y conversión a filas de tabla
├── vistas.py                Las cinco pantallas
│
├── models/
│   ├── mesa.py
│   ├── cliente.py
│   └── reserva.py           Contiene Reserva y Caminando
│
├── structures/
│   ├── cola_prioridad.py    Cola con prioridad sobre heapq
│   ├── cola.py              Cola FIFO sobre deque
│   ├── pila.py              Pila LIFO sobre lista
│   └── cola_circular.py     Cola circular implementada a mano
│
├── services/
│   ├── gestor_mesas.py
│   ├── gestor_clientes.py
│   └── gestor_reservas.py   Utiliza las cuatro estructuras
│
├── tests/                   Pruebas de cada estructura
├── run_tests.py
├── test_integracion_gui.py
├── test_sin_mocks.py
└── datos_mesaflow.json      Se genera automáticamente
```

---


## Posibles mejoras para fases siguientes

El proyecto quedó preparado para incorporar nuevas estructuras sin modificar la interfaz. Como la lógica está aislada en la capa de servicios, un cambio en esa capa no afecta a las pantallas.

Una mejora natural para la siguiente fase sería reemplazar la búsqueda lineal de reservas por un árbol balanceado, que reduciría el costo de buscar una reserva concreta de O(n) a O(log n). Otra posibilidad es incorporar una tabla hash para localizar las reservas de un cliente en tiempo constante. También se podría modelar el restaurante como un grafo, donde las mesas adyacentes entre sí permiten sugerir mesas alternativas cuando la asignada no resulte conveniente.

Estas modificaciones se limitarían a las capas de estructuras y servicios. La interfaz seguiría funcionando sin cambios.
