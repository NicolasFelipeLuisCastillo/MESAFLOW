import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import date, time, datetime

import datos

#  VISTA MESAS

class VistaMesas:
    def __init__(self, area_dinamica, app):
        self.area_dinamica = area_dinamica
        self.app = app

        self.area_dinamica.grid_columnconfigure(0, weight=1)
        self.area_dinamica.grid_columnconfigure(1, weight=3)
        self.area_dinamica.grid_rowconfigure(0, weight=1)

        #Formulario (izquierda)
        self.frame_form = ctk.CTkFrame(self.area_dinamica, fg_color=self.app.COLOR_BG_SOFT,
                                       border_color="#E5E7EB", border_width=1)
        self.frame_form.grid(row=0, column=0, padx=(0, 15), pady=10, sticky="nnew")

        ctk.CTkLabel(self.frame_form, text="Nueva Mesa",
                     font=("Inter", 15, "bold"), text_color="black").pack(pady=(15, 10), padx=15, anchor="w")

        ctk.CTkLabel(self.frame_form, text="Capacidad (personas):",
                     font=("Inter", 11), text_color="black").pack(padx=15, anchor="w")
        self.entry_capacidad = ctk.CTkEntry(self.frame_form, placeholder_text="Ej. 4",
                                            fg_color="white", text_color="black")
        self.entry_capacidad.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkLabel(self.frame_form, text="Ubicación:",
                     font=("Inter", 11), text_color="black").pack(padx=15, anchor="w")
        self.combo_ubicacion = ctk.CTkComboBox(self.frame_form,
                                               values=["Interior", "Exterior", "Ventana"],
                                               fg_color="white", text_color="black",
                                               dropdown_fg_color="white", dropdown_text_color="black")
        self.combo_ubicacion.pack(fill="x", padx=15, pady=(0, 20))

        ctk.CTkButton(self.frame_form, text="Agregar mesa", fg_color=self.app.COLOR_ACCENT,
                      hover_color="#7C2D12", font=("Inter", 12, "bold"),
                      command=self.agregar_mesa).pack(fill="x", padx=15, pady=(0, 20))

        #Tabla (derecha)
        self.frame_tabla = ctk.CTkFrame(self.area_dinamica, fg_color="transparent")
        self.frame_tabla.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.frame_tabla.grid_columnconfigure(0, weight=1)
        self.frame_tabla.grid_rowconfigure(1, weight=1)

        self.lbl_total = ctk.CTkLabel(self.frame_tabla, text="",
                                      font=("Inter", 13, "bold"), text_color="black")
        self.lbl_total.grid(row=0, column=0, sticky="w", pady=(0, 10))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Mesa.Treeview", background="white", fieldbackground="white",
                        rowheight=38, font=("Inter", 11))
        style.configure("Mesa.Treeview.Heading", background="#E5E7EB", font=("Inter", 11, "bold"))
        style.map("Mesa.Treeview", background=[("selected", self.app.COLOR_ACCENT)])

        self.tabla = ttk.Treeview(self.frame_tabla,
                                  columns=("ID", "Capacidad", "Ubicación", "Estado"),
                                  show="headings", style="Mesa.Treeview")
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Capacidad", text="Capacidad")
        self.tabla.heading("Ubicación", text="Ubicación")
        self.tabla.heading("Estado", text="Estado")

        self.tabla.column("ID", width=60, anchor="center")
        self.tabla.column("Capacidad", width=110, anchor="center")
        self.tabla.column("Ubicación", width=140, anchor="center")
        self.tabla.column("Estado", width=160, anchor="center")
        self.tabla.grid(row=1, column=0, sticky="nsew", pady=(0, 15))

        ctk.CTkButton(self.frame_tabla, text="Eliminar Mesa Seleccionada", fg_color="#DC2626",
                      hover_color="#991B1B", font=("Inter", 12, "bold"),
                      command=self.eliminar_mesa).grid(row=2, column=0, sticky="e")

        self.actualizar_tabla()

    def actualizar_tabla(self):
        #Pide las mesas al GESTOR y las dibuja en la tabla
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        # Acá se usa el servicio, no una lista suelta
        mesas = datos.mesas_para_tabla(self.app.gestor_mesas)

        for mesa in mesas:
            self.tabla.insert("", "end", values=(
                mesa["id"], mesa["capacidad"], mesa["ubicacion"], mesa["estado"]
            ))

        self.lbl_total.configure(text="Total: {} mesas".format(len(mesas)))

    def agregar_mesa(self):
        capacidad = self.entry_capacidad.get().strip()
        ubicacion = self.combo_ubicacion.get()

        if not capacidad.isdigit() or not (1 <= int(capacidad) <= 20):
            messagebox.showerror("Error de Validación",
                                 "La capacidad debe estar entre 1 y 20 personas.")
            return

        # Le pedimos la mesa al GESTOR
        mesa = self.app.gestor_mesas.agregar(capacidad, ubicacion)

        if mesa is None:
            messagebox.showerror("Error", "No se pudo agregar la mesa.")
            return

        # Como cambiaron las mesas, hay que rehacer la cola circular
        self.app.guardar_datos_sistema()
        self.actualizar_tabla()
        self.entry_capacidad.delete(0, "end")
        messagebox.showinfo("Éxito", "Mesa {} agregada correctamente.".format(mesa.id))

    def eliminar_mesa(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una mesa de la lista.")
            return

        valores = self.tabla.item(seleccion)["values"]
        id_mesa = valores[0]

        if messagebox.askyesno("Confirmar", "¿Deseas eliminar la mesa ID {}?".format(id_mesa)):
            # Le pedimos la eliminación al GESTOR
            if self.app.gestor_mesas.eliminar(id_mesa):
                self.app.guardar_datos_sistema()
                self.actualizar_tabla()
            else:
                messagebox.showerror("Error", "No se puede eliminar una mesa ocupada.")


#  VISTA CLIENTES
class VistaClientes:
    def __init__(self, area_dinamica, app):
        self.area_dinamica = area_dinamica
        self.app = app

        self.area_dinamica.grid_columnconfigure(0, weight=1)
        self.area_dinamica.grid_columnconfigure(1, weight=3)
        self.area_dinamica.grid_rowconfigure(0, weight=1)

        self.frame_form = ctk.CTkFrame(self.area_dinamica, fg_color=self.app.COLOR_BG_SOFT,
                                       border_color="#E5E7EB", border_width=1)
        self.frame_form.grid(row=0, column=0, padx=(0, 15), pady=10, sticky="nnew")

        ctk.CTkLabel(self.frame_form, text="Nuevo Cliente",
                     font=("Inter", 15, "bold"), text_color="black").pack(pady=10, padx=15, anchor="w")

        self.entry_nombre = ctk.CTkEntry(self.frame_form, placeholder_text="Nombre completo",
                                         fg_color="white", text_color="black")
        self.entry_nombre.pack(fill="x", padx=15, pady=5)

        self.entry_telefono = ctk.CTkEntry(self.frame_form, placeholder_text="Teléfono",
                                           fg_color="white", text_color="black")
        self.entry_telefono.pack(fill="x", padx=15, pady=5)

        self.var_vip = ctk.IntVar(value=0)
        ctk.CTkCheckBox(self.frame_form, text="Cliente VIP", variable=self.var_vip,
                        text_color="black", fg_color="#000000").pack(padx=15, pady=10, anchor="w")

        ctk.CTkButton(self.frame_form, text="Agregar cliente", fg_color=self.app.COLOR_ACCENT,
                      font=("Inter", 12, "bold"),
                      command=self.agregar_cliente).pack(fill="x", padx=15, pady=10)

        self.frame_tabla = ctk.CTkFrame(self.area_dinamica, fg_color="transparent")
        self.frame_tabla.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.frame_tabla.grid_columnconfigure(0, weight=1)
        self.frame_tabla.grid_rowconfigure(1, weight=1)

        self.lbl_total = ctk.CTkLabel(self.frame_tabla, text="",
                                      font=("Inter", 13, "bold"), text_color="black")
        self.lbl_total.grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.entry_buscar = ctk.CTkEntry(self.frame_tabla, placeholder_text="Buscar por nombre...",
                                         fg_color="white", text_color="black", width=200)
        self.entry_buscar.grid(row=0, column=0, sticky="e", pady=(0, 5))
        self.entry_buscar.bind("<KeyRelease>", lambda e: self.actualizar_tabla())

        style = ttk.Style()
        style.configure("Cliente.Treeview", background="white", fieldbackground="white",
                        rowheight=38, font=("Inter", 11))

        self.tabla = ttk.Treeview(self.frame_tabla,
                                  columns=("ID", "Nombre", "Teléfono", "VIP"),
                                  show="headings", style="Cliente.Treeview")
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Teléfono", text="Teléfono")
        self.tabla.heading("VIP", text="VIP")

        self.tabla.column("ID", width=50, anchor="center")
        self.tabla.column("Nombre", width=180, anchor="w")
        self.tabla.column("Teléfono", width=120, anchor="center")
        self.tabla.column("VIP", width=70, anchor="center")
        self.tabla.grid(row=1, column=0, sticky="nsew")

        ctk.CTkButton(self.frame_tabla, text="Eliminar Cliente Seleccionado", fg_color="#DC2626",
                      hover_color="#991B1B", font=("Inter", 12, "bold"),
                      command=self.eliminar_cliente).grid(row=2, column=0, sticky="e", pady=(10, 0))

        self.actualizar_tabla()

    def actualizar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        texto = self.entry_buscar.get().strip()

        # Si hay algo escrito, le pedimos al GESTOR que filtre
        if texto:
            clientes = datos.clientes_para_tabla(self.app.gestor_clientes)
            clientes = [c for c in clientes if texto.lower() in c["nombre"].lower()]
        else:
            clientes = datos.clientes_para_tabla(self.app.gestor_clientes)

        for cliente in clientes:
            self.tabla.insert("", "end", values=(
                cliente["id"], cliente["nombre"], cliente["telefono"], cliente["vip"]
            ))

        total = self.app.gestor_clientes.total_clientes()
        vips = self.app.gestor_clientes.total_vips()
        self.lbl_total.configure(text="Total: {} clientes ({} VIP)".format(total, vips))

    def agregar_cliente(self):
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()
        vip = self.var_vip.get() == 1

        if not nombre:
            messagebox.showerror("Error de Validación", "El nombre no puede estar vacío.")
            return
        if len(nombre) > 100:
            messagebox.showerror("Error de Validación", "El nombre supera los 100 caracteres.")
            return

        for caracter in telefono:
            if caracter.isdigit() is False and caracter not in ["-", " "]:
                messagebox.showerror("Error de Validación", "Formato de teléfono inválido.")
                return
        if not telefono or len(telefono) < 7 or len(telefono) > 15:
            messagebox.showerror("Error de Validación", "Formato de teléfono inválido.")
            return

        # Le pedimos el cliente al GESTOR
        cliente = self.app.gestor_clientes.agregar(nombre, telefono, vip)

        self.app.guardar_datos_sistema()
        self.actualizar_tabla()

        self.entry_nombre.delete(0, "end")
        self.entry_telefono.delete(0, "end")
        self.var_vip.set(0)
        messagebox.showinfo("Éxito", "Cliente '{}' agregado.".format(cliente.nombre))

    def eliminar_cliente(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un cliente de la lista.")
            return

        valores = self.tabla.item(seleccion)["values"]
        id_cliente = valores[0]
        nombre = valores[1]

        if messagebox.askyesno("Confirmar",
                               "¿Eliminar al cliente {} (ID: {})?".format(nombre, id_cliente)):
            if self.app.gestor_clientes.eliminar(id_cliente):
                self.app.guardar_datos_sistema()
                self.actualizar_tabla()
                messagebox.showinfo("Éxito", "Cliente '{}' eliminado.".format(nombre))


#  VISTA RESERVAS  (usa la COLA CON PRIORIDAD) — con pestañas Pendientes / En Curso
class VistaReservas:
    def __init__(self, area_dinamica, app):
        self.area_dinamica = area_dinamica
        self.app = app

        self.area_dinamica.grid_columnconfigure(0, weight=1)
        self.area_dinamica.grid_columnconfigure(1, weight=3)
        self.area_dinamica.grid_rowconfigure(1, weight=1)

        # ---- Formulario (izquierda, fila 1) ----
        self.frame_form = ctk.CTkFrame(self.area_dinamica, fg_color=self.app.COLOR_BG_SOFT,
                                       border_color="#E5E7EB", border_width=1)
        self.frame_form.grid(row=1, column=0, padx=(0, 15), pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_form, text="Nueva Reserva",
                     font=("Inter", 15, "bold"), text_color="black").pack(pady=10, padx=15, anchor="w")

        ctk.CTkLabel(self.frame_form, text="Seleccionar Cliente:",
                     font=("Inter", 11), text_color="black").pack(padx=15, anchor="w")
        nombres = [c.nombre for c in self.app.gestor_clientes.listar()] or ["No hay clientes"]
        self.combo_cliente = ctk.CTkComboBox(self.frame_form, values=nombres, fg_color="white",
                                             text_color="black", dropdown_fg_color="white",
                                             dropdown_text_color="black",
                                             command=self.verificar_cliente_vip)
        self.combo_cliente.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(self.frame_form, text="Seleccionar Mesa:",
                     font=("Inter", 11), text_color="black").pack(padx=15, anchor="w")
        ids_mesas = [str(m.id) for m in self.app.gestor_mesas.listar()] or ["1"]
        self.combo_mesa = ctk.CTkComboBox(self.frame_form, values=ids_mesas, fg_color="white",
                                          text_color="black", dropdown_fg_color="white",
                                          dropdown_text_color="black", state="disabled")
        self.combo_mesa.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(self.frame_form, text="(se asigna sola por round-robin)",
                     font=("Inter", 9, "italic"), text_color="#57534E").pack(padx=15, anchor="w")

        ctk.CTkLabel(self.frame_form, text="Hora (HH:MM):",
                     font=("Inter", 11), text_color="black").pack(padx=15, anchor="w")
        self.entry_hora = ctk.CTkEntry(self.frame_form, placeholder_text="Ej. 19:30",
                                       fg_color="white", text_color="black")
        self.entry_hora.pack(fill="x", padx=15, pady=5)

        ctk.CTkButton(self.frame_form, text="Crear reserva", fg_color=self.app.COLOR_ACCENT,
                      font=("Inter", 12, "bold"),
                      command=self.crear_reserva).pack(fill="x", padx=15, pady=15)

        # ---- Pestañas superiores (fila 0, columnas 0-1) ----
        self.pestanias = ctk.CTkSegmentedButton(
            self.area_dinamica, values=["Pendientes", "En Curso"],
            font=("Inter", 12, "bold"), fg_color="#E5E7EB",
            selected_color=self.app.COLOR_ACCENT, selected_hover_color="#7C2D12",
            unselected_color="#F5F5F4", unselected_hover_color="#D6D3D1",
            text_color="white", text_color_disabled="#57534E",
            command=self.cambiar_pestania
        )
        self.pestanias.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 5))
        self.pestania_actual = "Pendientes"

        # ---- Panel derecho (fila 1, columna 1) ----
        self.frame_tabla = ctk.CTkFrame(self.area_dinamica, fg_color="transparent")
        self.frame_tabla.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.frame_tabla.grid_columnconfigure(0, weight=1)
        self.frame_tabla.grid_rowconfigure(1, weight=1)

        self.lbl_contador = ctk.CTkLabel(self.frame_tabla, text="",
                                         font=("Inter", 13, "bold"), text_color="black")
        self.lbl_contador.grid(row=0, column=0, sticky="w", pady=(0, 5))

        style = ttk.Style()
        style.configure("Reserva.Treeview", background="white", fieldbackground="white",
                        rowheight=38, font=("Inter", 11))

        # Tabla de pendientes
        self.tabla = ttk.Treeview(self.frame_tabla,
                                  columns=("ID", "Cliente", "Mesa", "Hora", "Estado"),
                                  show="headings", style="Reserva.Treeview")
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Cliente", text="Cliente (orden de atención)")
        self.tabla.heading("Mesa", text="Mesa")
        self.tabla.heading("Hora", text="Hora")
        self.tabla.heading("Estado", text="Estado")
        self.tabla.column("ID", width=40, anchor="center")
        self.tabla.column("Cliente", width=150, anchor="w")
        self.tabla.column("Mesa", width=60, anchor="center")
        self.tabla.column("Hora", width=80, anchor="center")
        self.tabla.column("Estado", width=120, anchor="center")

        # Tabla de en curso
        self.tabla_en_curso = ttk.Treeview(self.frame_tabla,
                                  columns=("ID", "Cliente", "VIP", "Mesa", "Hora"),
                                  show="headings", style="Reserva.Treeview")
        self.tabla_en_curso.heading("ID", text="ID")
        self.tabla_en_curso.heading("Cliente", text="Cliente")
        self.tabla_en_curso.heading("VIP", text="VIP")
        self.tabla_en_curso.heading("Mesa", text="Mesa")
        self.tabla_en_curso.heading("Hora", text="Hora")
        self.tabla_en_curso.column("ID", width=40, anchor="center")
        self.tabla_en_curso.column("Cliente", width=160, anchor="w")
        self.tabla_en_curso.column("VIP", width=50, anchor="center")
        self.tabla_en_curso.column("Mesa", width=60, anchor="center")
        self.tabla_en_curso.column("Hora", width=80, anchor="center")

        # Botones de pendientes
        self.frame_botones_pend = ctk.CTkFrame(self.frame_tabla, fg_color="transparent")
        ctk.CTkButton(self.frame_botones_pend, text="Confirmar (En Curso)", fg_color="#15803D",
                      font=("Inter", 11, "bold"),
                      command=self.confirmar_reserva).pack(side="left", padx=5)
        ctk.CTkButton(self.frame_botones_pend, text="Cancelar Reserva", fg_color="#DC2626",
                      font=("Inter", 11, "bold"),
                      command=self.cancelar_reserva).pack(side="left", padx=5)

        # Botones de en curso
        self.frame_botones_curso = ctk.CTkFrame(self.frame_tabla, fg_color="transparent")
        ctk.CTkButton(self.frame_botones_curso, text="✓ Completar y Cobrar", fg_color="#7C3AED",
                      hover_color="#5B21B6", font=("Inter", 11, "bold"),
                      command=self.completar_reserva).pack(side="left", padx=5)

        self.pestanias.set("Pendientes")
        self.cambiar_pestania("Pendientes")

    def cambiar_pestania(self, valor):
        self.pestania_actual = valor

        # Ocultar todo
        self.tabla.grid_remove()
        self.tabla_en_curso.grid_remove()
        self.frame_botones_pend.grid_remove()
        self.frame_botones_curso.grid_remove()

        if valor == "Pendientes":
            self.frame_form.grid()
            self.tabla.grid(row=1, column=0, sticky="nsew")
            self.frame_botones_pend.grid(row=2, column=0, sticky="e", pady=(10, 0))
            self.actualizar_tabla()
        else:
            self.frame_form.grid_remove()
            self.tabla_en_curso.grid(row=1, column=0, sticky="nsew")
            self.frame_botones_curso.grid(row=2, column=0, sticky="e", pady=(10, 0))
            self.actualizar_tabla_en_curso()

    def verificar_cliente_vip(self, nombre):
        #Marco morado si el cliente elegido es VIP.
        cliente = self.app.gestor_clientes.obtener_por_nombre(nombre)
        if cliente is not None and cliente.es_vip:
            self.frame_form.configure(border_color="#7C3AED", border_width=2)
        else:
            self.frame_form.configure(border_color="#E5E7EB", border_width=1)

    def actualizar_tabla(self):

        #Dibuja las reservas PENDIENTES.

        #El orden de las filas lo pone la COLA CON PRIORIDAD
        #(datos.reservas_para_tabla), no un ordenamiento manual.

        if hasattr(self, "_refresco_id"):
            try:
                self.area_dinamica.after_cancel(self._refresco_id)
            except Exception:
                pass

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        reservas = datos.reservas_para_tabla(self.app.gestor_reservas,
                                            self.app.gestor_clientes)

        for reserva in reservas:
            if reserva["vip"] == "X":
                texto_cliente = "[VIP] " + reserva["cliente"]
            else:
                texto_cliente = reserva["cliente"]

            self.tabla.insert("", "end", values=(
                reserva["id"], texto_cliente, reserva["mesa"],
                reserva["hora"], reserva["estado"]
            ))

        pendientes = self.app.gestor_reservas.total_pendientes()
        en_curso = len(self.app.gestor_reservas.listar_en_curso())
        self.lbl_contador.configure(
            text="Pendientes: {}  |  En curso: {}".format(pendientes, en_curso))

        # Se refresca solo cada 3 segundos
        if self.pestania_actual == "Pendientes":
            self._refresco_id = self.area_dinamica.after(3000, self.actualizar_tabla)

    def actualizar_tabla_en_curso(self):
        #Dibuja las reservas EN CURSO (cliente sentado).

        if hasattr(self, "_refresco_id"):
            try:
                self.area_dinamica.after_cancel(self._refresco_id)
            except Exception:
                pass

        for fila in self.tabla_en_curso.get_children():
            self.tabla_en_curso.delete(fila)

        en_curso = datos.reservas_en_curso_para_tabla(self.app.gestor_reservas,
                                                      self.app.gestor_clientes)

        for reserva in en_curso:
            self.tabla_en_curso.insert("", "end", values=(
                reserva["id"], reserva["cliente"], reserva["vip"],
                reserva["mesa"], reserva["hora"]
            ))

        pendientes = self.app.gestor_reservas.total_pendientes()
        total_curso = len(en_curso)
        self.lbl_contador.configure(
            text="Pendientes: {}  |  En curso: {}".format(pendientes, total_curso))

        if self.pestania_actual == "En Curso":
            self._refresco_id = self.area_dinamica.after(3000, self.actualizar_tabla_en_curso)

    def leer_hora(self, texto):
        #Convierte 'HH:MM' en un objeto time. Devuelve None si no sirve.
        partes = texto.split(":")
        if len(partes) != 2:
            return None

        try:
            hora = int(partes[0].strip())
            minuto = int(partes[1].strip())
        except ValueError:
            return None

        if hora < 0 or hora > 23 or minuto < 0 or minuto > 59:
            return None

        # Horario del restaurante: 12:00 a 23:00
        if hora < 12:
            return None
        if hora == 23 and minuto > 0:
            return None

        return time(hora, minuto)

    def crear_reserva(self):
        nombre_cliente = self.combo_cliente.get()
        texto_hora = self.entry_hora.get().strip()

        hora = self.leer_hora(texto_hora)
        if hora is None:
            messagebox.showerror("Error de Validación",
                                 "El restaurante atiende de 12:00 a 23:00. Usa formato HH:MM.")
            return

        cliente = self.app.gestor_clientes.obtener_por_nombre(nombre_cliente)
        if cliente is None:
            messagebox.showerror("Error", "Ese cliente no existe.")
            return
        #  ROUND-ROBIN: la mesa la decide la COLA CIRCULAR

        mesa = self.app.gestor_reservas.siguiente_mesa()

        if mesa is None:
            messagebox.showerror("Error de Sistema", "No hay mesas registradas.")
            return

        # Chequeamos que la mesa esté libre en ese horario
        if not self.app.gestor_reservas.mesa_esta_libre(mesa.id, date.today(), hora, 90):
            messagebox.showerror("Choque de Horario",
                                 "La mesa {} ya tiene reserva en esa franja.".format(mesa.id))
            return

        # Le pedimos la reserva al GESTOR (que la mete a la cola con prioridad)
        reserva = self.app.gestor_reservas.crear_reserva(
            cliente.id, mesa.id, date.today(), hora, 90
        )

        self.combo_mesa.set(str(mesa.id))
        self.app.guardar_datos_sistema()
        self.actualizar_tabla()
        self.entry_hora.delete(0, "end")

        etiqueta = " (VIP)" if cliente.es_vip else ""
        messagebox.showinfo("Éxito",
                            "Reserva creada para {}{}.\nEl round-robin asignó la Mesa {}."
                            .format(cliente.nombre, etiqueta, mesa.id))

    def confirmar_reserva(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una reserva de la tabla.")
            return

        id_reserva = self.tabla.item(seleccion)["values"][0]

        # Le pedimos el cambio de estado al GESTOR
        if self.app.gestor_reservas.confirmar(id_reserva):
            self.app.guardar_datos_sistema()
            self.actualizar_tabla()
            messagebox.showinfo("Éxito", "La reserva ahora está En curso.\nLa mesa fue marcada como Ocupada.")
        else:
            messagebox.showerror("Error", "Esa reserva no se puede confirmar.")

    def completar_reserva(self):
        #Completa la reserva: libera la mesa y mueve al historial de atenciones.
        seleccion = self.tabla_en_curso.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una reserva en curso.")
            return

        id_reserva = self.tabla_en_curso.item(seleccion)["values"][0]

        if messagebox.askyesno("Confirmar", "¿Completar y cobrar esta reserva?\nLa mesa quedará libre."):
            if self.app.gestor_reservas.completar(id_reserva):
                self.app.guardar_datos_sistema()
                self.actualizar_tabla_en_curso()
                messagebox.showinfo("Completada", "Servicio finalizado. Mesa liberada.")
            else:
                messagebox.showerror("Error", "No se pudo completar esa reserva.")

    def cancelar_reserva(self):

        #Cancela la reserva.

        #El GESTOR la mete en la PILA de historial,
        #y ahí aparece sola en la pestaña Historial.

        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una reserva de la tabla.")
            return

        id_reserva = self.tabla.item(seleccion)["values"][0]

        if messagebox.askyesno("Confirmar", "¿Seguro que deseas cancelar esta reserva?"):
            if self.app.gestor_reservas.cancelar(id_reserva):
                self.app.guardar_datos_sistema()
                self.actualizar_tabla()
                messagebox.showinfo("Cancelada", "Reserva movida al historial.")

#  VISTA CAMINANDO  (Cola FIFO) — con pestañas En Espera / En Mesa
class VistaCaminando:
    def __init__(self, area_dinamica, app):
        self.area_dinamica = area_dinamica
        self.app = app

        self.area_dinamica.grid_columnconfigure(0, weight=1)
        self.area_dinamica.grid_columnconfigure(1, weight=3)
        self.area_dinamica.grid_rowconfigure(1, weight=1)

        # ---- Formulario (izquierda, fila 1) ----
        self.frame_form = ctk.CTkFrame(self.area_dinamica, fg_color=self.app.COLOR_BG_SOFT,
                                       border_color="#E5E7EB", border_width=1)
        self.frame_form.grid(row=1, column=0, padx=(0, 15), pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_form, text="Registro sin Reserva",
                     font=("Inter", 15, "bold"), text_color="black").pack(pady=10, padx=15, anchor="w")

        ctk.CTkLabel(self.frame_form, text="Cliente:", font=("Inter", 11),
                     text_color="black").pack(padx=15, anchor="w")
        nombres = [c.nombre for c in self.app.gestor_clientes.listar()] or ["Cliente General"]
        self.combo_cliente = ctk.CTkComboBox(self.frame_form, values=nombres, fg_color="white",
                                             text_color="black", dropdown_fg_color="white",
                                             dropdown_text_color="black")
        self.combo_cliente.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(self.frame_form, text="Nº de Personas:", font=("Inter", 11),
                     text_color="black").pack(padx=15, anchor="w")
        self.entry_personas = ctk.CTkEntry(self.frame_form, placeholder_text="Ej. 3",
                                           fg_color="white", text_color="black")
        self.entry_personas.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(self.frame_form, text="Hora Llegada (HH:MM):", font=("Inter", 11),
                     text_color="black").pack(padx=15, anchor="w")
        self.entry_hora = ctk.CTkEntry(self.frame_form, placeholder_text="Ej. 19:15",
                                       fg_color="white", text_color="black")
        self.entry_hora.pack(fill="x", padx=15, pady=5)

        ctk.CTkButton(self.frame_form, text="Agregar a la cola", fg_color=self.app.COLOR_ACCENT,
                      font=("Inter", 12, "bold"),
                      command=self.agregar_a_cola).pack(fill="x", padx=15, pady=15)

        # ---- Pestañas superiores ----
        self.pestanias = ctk.CTkSegmentedButton(
            self.area_dinamica, values=["En Espera", "En Mesa"],
            font=("Inter", 12, "bold"), fg_color="#E5E7EB",
            selected_color=self.app.COLOR_ACCENT, selected_hover_color="#7C2D12",
            unselected_color="#F5F5F4", unselected_hover_color="#D6D3D1",
            text_color="white", text_color_disabled="#57534E",
            command=self.cambiar_pestania
        )
        self.pestanias.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 5))
        self.pestania_actual = "En Espera"

        # ---- Panel derecho ----
        self.frame_tabla = ctk.CTkFrame(self.area_dinamica, fg_color="transparent")
        self.frame_tabla.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.frame_tabla.grid_columnconfigure(0, weight=1)
        self.frame_tabla.grid_rowconfigure(1, weight=1)

        self.lbl_contador = ctk.CTkLabel(self.frame_tabla, text="",
                                         font=("Inter", 13, "bold"), text_color="black")
        self.lbl_contador.grid(row=0, column=0, sticky="w", pady=(0, 5))

        style = ttk.Style()
        style.configure("Caminando.Treeview", background="white", fieldbackground="white",
                        rowheight=38, font=("Inter", 11))

        # Tabla de espera (FIFO)
        self.tabla = ttk.Treeview(self.frame_tabla,
                                  columns=("Pos", "Cliente", "Personas", "Hora"),
                                  show="headings", style="Caminando.Treeview")
        self.tabla.heading("Pos", text="Pos.")
        self.tabla.heading("Cliente", text="Cliente")
        self.tabla.heading("Personas", text="Personas")
        self.tabla.heading("Hora", text="Hora de llegada")
        self.tabla.column("Pos", width=50, anchor="center")
        self.tabla.column("Cliente", width=180, anchor="w")
        self.tabla.column("Personas", width=80, anchor="center")
        self.tabla.column("Hora", width=120, anchor="center")

        # Tabla de en mesa (sentados sin reserva)
        self.tabla_en_mesa = ttk.Treeview(self.frame_tabla,
                                  columns=("ID", "Cliente", "Personas", "Mesa", "Hora"),
                                  show="headings", style="Caminando.Treeview")
        self.tabla_en_mesa.heading("ID", text="ID")
        self.tabla_en_mesa.heading("Cliente", text="Cliente")
        self.tabla_en_mesa.heading("Personas", text="Personas")
        self.tabla_en_mesa.heading("Mesa", text="Mesa")
        self.tabla_en_mesa.heading("Hora", text="Hora llegada")
        self.tabla_en_mesa.column("ID", width=40, anchor="center")
        self.tabla_en_mesa.column("Cliente", width=160, anchor="w")
        self.tabla_en_mesa.column("Personas", width=80, anchor="center")
        self.tabla_en_mesa.column("Mesa", width=60, anchor="center")
        self.tabla_en_mesa.column("Hora", width=100, anchor="center")

        # Botón de espera
        self.frame_btn_espera = ctk.CTkFrame(self.frame_tabla, fg_color="transparent")
        ctk.CTkButton(self.frame_btn_espera, text="Atender sig.", fg_color="#15803D",
                      hover_color="#14532D", font=("Inter", 12, "bold"),
                      command=self.atender_siguiente).pack(side="left", padx=5)

        # Botón de en mesa
        self.frame_btn_mesa = ctk.CTkFrame(self.frame_tabla, fg_color="transparent")
        ctk.CTkButton(self.frame_btn_mesa, text="✓ Liberar Mesa y Cobrar", fg_color="#7C3AED",
                      hover_color="#5B21B6", font=("Inter", 12, "bold"),
                      command=self.finalizar_caminando).pack(side="left", padx=5)

        self.pestanias.set("En Espera")
        self.cambiar_pestania("En Espera")

    def cambiar_pestania(self, valor):
        self.pestania_actual = valor

        self.tabla.grid_remove()
        self.tabla_en_mesa.grid_remove()
        self.frame_btn_espera.grid_remove()
        self.frame_btn_mesa.grid_remove()

        if valor == "En Espera":
            self.frame_form.grid()
            self.tabla.grid(row=1, column=0, sticky="nsew")
            self.frame_btn_espera.grid(row=2, column=0, sticky="e", pady=(10, 0))
            self.actualizar_tabla()
        else:
            self.frame_form.grid_remove()
            self.tabla_en_mesa.grid(row=1, column=0, sticky="nsew")
            self.frame_btn_mesa.grid(row=2, column=0, sticky="e", pady=(10, 0))
            self.actualizar_tabla_en_mesa()

    def actualizar_tabla(self):
        #El orden lo da la COLA FIFO, no un sort()
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        fila_datos = datos.caminando_para_tabla(self.app.gestor_reservas,
                                               self.app.gestor_clientes)

        for fila in fila_datos:
            self.tabla.insert("", "end", values=(
                fila["pos"], fila["cliente"], fila["personas"], fila["hora"]
            ))

        en_espera = len(fila_datos)
        en_mesa = len(self.app.gestor_reservas.listar_caminando_en_mesa())
        self.lbl_contador.configure(
            text="En espera: {} grupos  |  En mesa: {}".format(en_espera, en_mesa))

    def actualizar_tabla_en_mesa(self):
        #Los que están sentados sin reserva.
        for fila in self.tabla_en_mesa.get_children():
            self.tabla_en_mesa.delete(fila)

        fila_datos = datos.caminando_en_mesa_para_tabla(self.app.gestor_reservas,
                                                        self.app.gestor_clientes)

        for fila in fila_datos:
            self.tabla_en_mesa.insert("", "end", values=(
                fila["id"], fila["cliente"], fila["personas"],
                fila["mesa"], fila["hora"]
            ))

        en_espera = self.app.gestor_reservas.total_caminando()
        en_mesa = len(fila_datos)
        self.lbl_contador.configure(
            text="En espera: {} grupos  |  En mesa: {}".format(en_espera, en_mesa))

    def agregar_a_cola(self):
        nombre_cliente = self.combo_cliente.get()
        personas = self.entry_personas.get().strip()
        hora_texto = self.entry_hora.get().strip()

        if not personas.isdigit():
            messagebox.showerror("Error", "Personas debe ser un número.")
            return

        # Reusa la validación de hora de las reservas
        partes = hora_texto.split(":")
        try:
            hora_num = int(partes[0])
            minuto_num = int(partes[1])
            if hora_num < 12 or hora_num > 23 or (hora_num == 23 and minuto_num > 0):
                raise ValueError()
        except (ValueError, IndexError):
            messagebox.showerror("Error de Validación",
                                 "El restaurante atiende de 12:00 a 23:00.")
            return

        cliente = self.app.gestor_clientes.obtener_por_nombre(nombre_cliente)
        if cliente is None:
            messagebox.showerror("Error", "Ese cliente no existe.")
            return

        # Le pedimos al GESTOR que lo meta a la COLA FIFO
        self.app.gestor_reservas.agregar_caminando(
            cliente.id, int(personas), hora_texto
        )

        self.app.guardar_datos_sistema()
        self.actualizar_tabla()

        self.entry_personas.delete(0, "end")
        self.entry_hora.delete(0, "end")
        messagebox.showinfo("Éxito", "{} agregado a la cola".format(cliente.nombre))

    def atender_siguiente(self):
        #Saca el primero de la cola FIFO, le asigna mesa y lo sienta.
        atendido = self.app.gestor_reservas.atender_caminando()

        if atendido is None:
            messagebox.showwarning("Cola vacía", "No hay clientes en espera.")
            return

        cliente = self.app.gestor_clientes.obtener(atendido.cliente_id)
        nombre = cliente.nombre if cliente is not None else "el cliente"

        mesa_texto = ""
        if atendido.mesa_id is not None:
            mesa_texto = "\nSe le asignó la Mesa {}.".format(atendido.mesa_id)

        self.app.guardar_datos_sistema()
        self.actualizar_tabla()
        messagebox.showinfo("Atención", "¡Atendiste a {}!{}".format(nombre, mesa_texto))

    def finalizar_caminando(self):
        #Libera la mesa y mueve al historial de atenciones.
        seleccion = self.tabla_en_mesa.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un cliente de la tabla.")
            return

        valores = self.tabla_en_mesa.item(seleccion)["values"]
        id_caminando = valores[0]  # columna "ID"

        if messagebox.askyesno("Confirmar", "¿Finalizar servicio y liberar la mesa?"):
            resultado = self.app.gestor_reservas.finalizar_caminando(id_caminando)
            if resultado is not None:
                self.app.guardar_datos_sistema()
                self.actualizar_tabla_en_mesa()
                messagebox.showinfo("Finalizado", "Mesa liberada. Servicio registrado en atenciones.")
            else:
                messagebox.showerror("Error", "No se pudo finalizar ese servicio.")

#  VISTA HISTORIAL  (Pila LIFO) — con pestañas Cancelaciones / Atenciones
class VistaHistorial:
    def __init__(self, area_dinamica, app):
        self.area_dinamica = area_dinamica
        self.app = app

        self.area_dinamica.grid_columnconfigure(0, weight=1)
        self.area_dinamica.grid_rowconfigure(2, weight=1)

        # ---- Pestañas superiores ----
        self.pestanias = ctk.CTkSegmentedButton(
            self.area_dinamica, values=["Cancelaciones", "Atenciones"],
            font=("Inter", 12, "bold"), fg_color="#E5E7EB",
            selected_color=self.app.COLOR_ACCENT, selected_hover_color="#7C2D12",
            unselected_color="#F5F5F4", unselected_hover_color="#D6D3D1",
            text_color="white", text_color_disabled="#57534E",
            command=self.cambiar_pestania
        )
        self.pestanias.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 5))
        self.pestania_actual = "Cancelaciones"

        self.lbl_total = ctk.CTkLabel(self.area_dinamica, text="",
                                      font=("Inter", 13, "bold"), text_color="black")
        self.lbl_total.grid(row=1, column=0, sticky="w", pady=(0, 10))

        self.lbl_vacio = ctk.CTkLabel(self.area_dinamica, text="",
                                      font=("Inter", 14, "italic"), text_color="#57534E")

        style = ttk.Style()
        style.configure("Historial.Treeview", background="white", fieldbackground="white",
                        rowheight=38, font=("Inter", 11))

        # Tabla de cancelaciones (pila historial)
        self.tabla = ttk.Treeview(self.area_dinamica,
                                  columns=("ID", "Cliente", "Mesa", "Fecha", "Hora", "Cancelada"),
                                  show="headings", style="Historial.Treeview")
        self.tabla.heading("ID", text="#")
        self.tabla.heading("Cliente", text="Cliente")
        self.tabla.heading("Mesa", text="Mesa")
        self.tabla.heading("Fecha", text="Fecha")
        self.tabla.heading("Hora", text="Hora")
        self.tabla.heading("Cancelada", text="Cancelada")
        self.tabla.column("ID", width=50, anchor="center")
        self.tabla.column("Cliente", width=180, anchor="w")
        self.tabla.column("Mesa", width=60, anchor="center")
        self.tabla.column("Fecha", width=110, anchor="center")
        self.tabla.column("Hora", width=80, anchor="center")
        self.tabla.column("Cancelada", width=120, anchor="center")

        # Tabla de atenciones (pila atenciones)
        self.tabla_atenciones = ttk.Treeview(self.area_dinamica,
                                  columns=("ID", "Tipo", "Cliente", "Mesa", "Fecha", "Hora"),
                                  show="headings", style="Historial.Treeview")
        self.tabla_atenciones.heading("ID", text="#")
        self.tabla_atenciones.heading("Tipo", text="Tipo")
        self.tabla_atenciones.heading("Cliente", text="Cliente")
        self.tabla_atenciones.heading("Mesa", text="Mesa")
        self.tabla_atenciones.heading("Fecha", text="Fecha")
        self.tabla_atenciones.heading("Hora", text="Hora")
        self.tabla_atenciones.column("ID", width=50, anchor="center")
        self.tabla_atenciones.column("Tipo", width=100, anchor="center")
        self.tabla_atenciones.column("Cliente", width=160, anchor="w")
        self.tabla_atenciones.column("Mesa", width=60, anchor="center")
        self.tabla_atenciones.column("Fecha", width=110, anchor="center")
        self.tabla_atenciones.column("Hora", width=80, anchor="center")

        self.pestanias.set("Cancelaciones")
        self.cambiar_pestania("Cancelaciones")

    def cambiar_pestania(self, valor):
        self.pestania_actual = valor

        self.tabla.grid_remove()
        self.tabla_atenciones.grid_remove()
        self.lbl_vacio.grid_remove()

        if valor == "Cancelaciones":
            self.actualizar_tabla_cancelaciones()
        else:
            self.actualizar_tabla_atenciones()

    def actualizar_tabla_cancelaciones(self):

        #El orden de la tabla lo pone la PILA LIFO:
        #la cancelación más reciente arriba.

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        historial = datos.historial_para_tabla(self.app.gestor_reservas,
                                              self.app.gestor_clientes)

        if len(historial) == 0:
            self.tabla.grid_remove()
            self.lbl_vacio.configure(text="Aún no hay cancelaciones 📂")
            self.lbl_vacio.grid(row=2, column=0, pady=40, sticky="n")
            self.lbl_total.configure(text="Total de cancelaciones: 0")
            return

        self.lbl_vacio.grid_remove()
        self.tabla.grid(row=2, column=0, sticky="nsew")

        for cancelacion in historial:
            self.tabla.insert("", "end", values=(
                cancelacion["id"], cancelacion["cliente"], cancelacion["mesa"],
                cancelacion["fecha"], cancelacion["hora"], cancelacion["tiempo"]
            ))

        self.lbl_total.configure(
            text="Total de cancelaciones: {}".format(len(historial)))

    def actualizar_tabla_atenciones(self):

        #El orden de la tabla lo pone la PILA LIFO (pila_atenciones):
        #el servicio más reciente arriba.

        for fila in self.tabla_atenciones.get_children():
            self.tabla_atenciones.delete(fila)

        atenciones = datos.atenciones_para_tabla(self.app.gestor_reservas,
                                                 self.app.gestor_clientes)

        if len(atenciones) == 0:
            self.tabla_atenciones.grid_remove()
            self.lbl_vacio.configure(text="Aún no hay servicios completados 📋")
            self.lbl_vacio.grid(row=2, column=0, pady=40, sticky="n")
            self.lbl_total.configure(text="Total de atenciones: 0")
            return

        self.lbl_vacio.grid_remove()
        self.tabla_atenciones.grid(row=2, column=0, sticky="nsew")

        for atencion in atenciones:
            self.tabla_atenciones.insert("", "end", values=(
                atencion["id"], atencion["tipo"], atencion["cliente"],
                atencion["mesa"], atencion["fecha"], atencion["hora"]
            ))

        self.lbl_total.configure(
            text="Total de atenciones: {}".format(len(atenciones)))