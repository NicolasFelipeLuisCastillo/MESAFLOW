import customtkinter as ctk

#Los servicios (la lógica de negocio)
from services.gestor_mesas import GestorMesas
from services.gestor_clientes import GestorClientes
from services.gestor_reservas import GestorReservas

#El puente con el JSON y las tablas
import datos

#Las 5 pantallas
from vistas import VistaMesas, VistaClientes, VistaReservas, VistaCaminando, VistaHistorial

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


def cargar_datos_iniciales(gestor_mesas, gestor_clientes, gestor_reservas):

    #Primero intenta leer el JSON. Si no existe, carga datos de ejemplo
    #para que la app no arranque vacía.

    se_cargo = datos.cargar_sistema(gestor_mesas, gestor_clientes, gestor_reservas)

    if se_cargo:
        return

    # No hay JSON, entonces ponemos datos de ejemplo
    gestor_mesas.agregar(2, "ventana")
    gestor_mesas.agregar(4, "interior")
    gestor_mesas.agregar(4, "interior")
    gestor_mesas.agregar(6, "exterior")

    gestor_clientes.agregar("Juan P.", "555-1234", False)
    gestor_clientes.agregar("Ana L.", "555-5678", True)
    gestor_clientes.agregar("Carlos R.", "555-9012", False)


class MesaFlowApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MesaFlow — Sistema de Reservas")
        self.geometry("1100x700")

        # Colores
        self.COLOR_ACCENT = "#C2410C"
        self.COLOR_SIDEBAR_BG = "#1C1917"
        self.COLOR_PAPER = "#FAFAF9"
        self.COLOR_BG_SOFT = "#FFF7ED"

        #  PASO 1: CREAMOS LOS SERVICIOS
        #  Acá es donde nacen las estructuras de datos
        self.gestor_mesas = GestorMesas()
        self.gestor_clientes = GestorClientes()
        self.gestor_reservas = GestorReservas(self.gestor_mesas, self.gestor_clientes)

        #  PASO 2: CARGAMOS LOS DATOS
        cargar_datos_iniciales(self.gestor_mesas, self.gestor_clientes, self.gestor_reservas)

        #  PASO 3: ARMAMOS LA VENTANA
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0,
                                    fg_color=self.COLOR_SIDEBAR_BG)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(self.sidebar, text="MesaFlow 1.0", text_color="white",
                     font=("Inter", 18, "bold")).pack(pady=20)

        self.botones = {}
        for nombre in ["Inicio", "Mesas", "Clientes", "Reservas", "Caminando", "Historial"]:
            boton = ctk.CTkButton(
                self.sidebar, text=nombre, fg_color="transparent", text_color="white",
                anchor="w", font=("Inter", 12, "bold"),
                command=lambda v=nombre: self.cambiar_vista(v)
            )
            boton.pack(fill="x", padx=10, pady=4)
            self.botones[nombre] = boton

        # Panel derecho
        self.contenido = ctk.CTkFrame(self, corner_radius=0, fg_color=self.COLOR_PAPER)
        self.contenido.grid(row=0, column=1, sticky="nsew")
        self.contenido.grid_columnconfigure(0, weight=1)
        self.contenido.grid_rowconfigure(1, weight=1)

        self.titulo = ctk.CTkLabel(self.contenido, text="Inicio", text_color="black",
                                   font=("Inter", 24, "bold"))
        self.titulo.grid(row=0, column=0, sticky="w", padx=24, pady=20)

        self.area_dinamica = ctk.CTkFrame(self.contenido, fg_color="transparent")
        self.area_dinamica.grid(row=1, column=0, sticky="nsew", padx=24, pady=10)

        self.vista_actual = "Inicio"

        # Atajos
        self.bind("<Control-q>", lambda e: self.destroy())
        self.bind("<Control-Q>", lambda e: self.destroy())
        self.bind("<F5>", lambda e: self.cambiar_vista(self.vista_actual))

        self.cambiar_vista("Inicio")

    def guardar_datos_sistema(self):
        #Le pide al puente que escriba todo en el JSON
        datos.guardar_sistema(self.gestor_mesas, self.gestor_clientes, self.gestor_reservas)

    def cambiar_vista(self, nombre):
        self.vista_actual = nombre
        self.titulo.configure(text=nombre)

        for widget in self.area_dinamica.winfo_children():
            widget.destroy()

        for nombre_vista, boton in self.botones.items():
            if nombre_vista == nombre:
                boton.configure(fg_color=self.COLOR_ACCENT)
            else:
                boton.configure(fg_color="transparent")

        # Cada vista recibe el `self`, y de ahí saca los servicios
        if nombre == "Inicio":
            ctk.CTkLabel(self.area_dinamica, text="¡Bienvenido a MesaFlow!",
                         font=("Inter", 14), text_color="black").pack(pady=40)

            ctk.CTkLabel(self.area_dinamica,
                         text="Mesas: {}   |   Clientes: {}   |   Pendientes: {}".format(
                             self.gestor_mesas.total_mesas(),
                             self.gestor_clientes.total_clientes(),
                             self.gestor_reservas.total_pendientes()),
                         font=("Inter", 12), text_color="#57534E").pack()

        elif nombre == "Mesas":
            VistaMesas(self.area_dinamica, self)
        elif nombre == "Clientes":
            VistaClientes(self.area_dinamica, self)
        elif nombre == "Reservas":
            VistaReservas(self.area_dinamica, self)
        elif nombre == "Caminando":
            VistaCaminando(self.area_dinamica, self)
        elif nombre == "Historial":
            VistaHistorial(self.area_dinamica, self)


if __name__ == "__main__":
    app = MesaFlowApp()
    app.mainloop()