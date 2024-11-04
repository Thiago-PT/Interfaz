import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
import requests
from io import BytesIO
from formularios.form_reconocimiento import mostrar_ventana_reconocimiento
from formularios.form_panel_datos import mostrar_panel_datos
from formularios.form_salir import salir_aplicacion

# Definición de colores modernos
COLOR_BARRA_SUPERIOR = "#1a1b26"    # Azul oscuro
COLOR_MENU_LATERAL = "#2d4f7c"      # Azul medio
COLOR_CUERPO_PRINCIPAL = "#f0f5ff"  # Azul claro
COLOR_HOVER = "#1a365d"             # Azul oscuro para hover

# URLs de Google Drive convertidas a enlaces directos
LOGO_URL = "https://drive.google.com/uc?export=view&id=19Ohw-T6nyFb3ENL0PLUQf2kI73C5eBPZ"
PERFIL_URL = "https://drive.google.com/uc?export=view&id=1D4OPybTHAjialmRe44ONqiip-TG4gY_c"

class FormularioMaestroDesign(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configurar tema
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        # Inicializar variables de instancia
        self.logo = None
        self.perfil = None
        self.menu_lateral = None
        self.cuerpo_principal = None
        
        try:
            # Cargar logo desde URL
            response = requests.get(LOGO_URL)
            self.logo = ImageTk.PhotoImage(Image.open(BytesIO(response.content)))
        except Exception as e:
            print(f"Error al cargar el logo: {e}")
        
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.cargar_pantalla_principal()

    def config_window(self):
        self.title('Eye System - Maestro')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height-40}+0+0")
        self.resizable(True, True)

    def paneles(self):
        # Barra superior
        self.barra_superior = ctk.CTkFrame(self, fg_color=COLOR_BARRA_SUPERIOR, height=60)
        self.barra_superior.pack(side='top', fill='x')
        
        # Contenedor principal
        self.contenedor_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_principal.pack(side='top', fill='both', expand=True)
        
        self.contenedor_principal.grid_columnconfigure(1, weight=1)
        self.contenedor_principal.grid_rowconfigure(0, weight=1)
        
        # Menú lateral
        self.menu_lateral = ctk.CTkFrame(self.contenedor_principal, fg_color=COLOR_MENU_LATERAL, width=250)
        self.menu_lateral.grid(row=0, column=0, sticky="nsew")
        self.menu_lateral.grid_propagate(False)
        
        # Cuerpo principal
        self.cuerpo_principal = ctk.CTkFrame(self.contenedor_principal, fg_color=COLOR_CUERPO_PRINCIPAL)
        self.cuerpo_principal.grid(row=0, column=1, sticky="nsew")

    def controles_barra_superior(self):
        self.label_titulo = ctk.CTkLabel(
            self.barra_superior,
            text="Eye System - Maestro",
            font=("Roboto", 20, "bold"),
            text_color="white"
        )
        self.label_titulo.pack(side='left', padx=20)
        
        self.button_menu = ctk.CTkButton(
            self.barra_superior,
            text="≡",
            width=40,
            command=self.toggle_panel,
            fg_color="transparent",
            hover_color=COLOR_HOVER
        )
        self.button_menu.pack(side='left', padx=10)

    def controles_menu_lateral(self):
        try:
            # Cargar imagen de perfil desde URL
            response = requests.get(PERFIL_URL)
            perfil_img = Image.open(BytesIO(response.content))
            perfil_img = perfil_img.resize((100, 100))
            self.perfil = ImageTk.PhotoImage(self.create_circular_image(perfil_img))
            
            label_perfil = ctk.CTkLabel(self.menu_lateral, image=self.perfil, text="")
            label_perfil.pack(pady=20)
        except Exception as e:
            print(f"Error al cargar la imagen de perfil: {e}")

        botones_info = [
            ("Reconocimiento", lambda: self.abrir_pantalla(mostrar_ventana_reconocimiento)),
            ("Panel De Datos", lambda: self.abrir_pantalla(mostrar_panel_datos)),
            ("Salir", lambda: salir_aplicacion(self))
        ]

        for texto, comando in botones_info:
            btn = ctk.CTkButton(
                self.menu_lateral,
                text=texto,
                command=comando,
                width=200,
                height=40,
                corner_radius=10,
                fg_color="transparent",
                hover_color=COLOR_HOVER,
                border_width=2,
                border_color="white"
            )
            btn.pack(pady=10, padx=20)

    def cargar_pantalla_principal(self, frame_principal=None):
        self.toggle_panel(True)
        if frame_principal is None:
            frame_principal = self.cuerpo_principal
            
        for widget in frame_principal.winfo_children():
            widget.destroy()
        
        frame_width = frame_principal.winfo_width()
        frame_height = frame_principal.winfo_height()
        
        if frame_width <= 1 or frame_height <= 1:
            frame_width = 800
            frame_height = 600
        
        try:
            # Cargar y redimensionar logo desde URL
            response = requests.get(LOGO_URL)
            original_image = Image.open(BytesIO(response.content))
            aspect_ratio = original_image.width / original_image.height
            
            if frame_width / frame_height > aspect_ratio:
                new_height = frame_height
                new_width = int(frame_height * aspect_ratio)
            else:
                new_width = frame_width
                new_height = int(frame_width / aspect_ratio)
            
            resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(resized_image)
            
            label_logo = ctk.CTkLabel(frame_principal, image=self.logo, text="")
            label_logo.place(relx=0.5, rely=0.5, anchor='center')
            
            frame_principal.bind('<Configure>', lambda e: self.actualizar_imagen(e, label_logo))
        except Exception as e:
            print(f"Error al cargar o redimensionar el logo: {e}")

    def actualizar_imagen(self, event, label_logo):
        try:
            frame_width = event.width
            frame_height = event.height
            
            # Cargar y redimensionar logo desde URL
            response = requests.get(LOGO_URL)
            original_image = Image.open(BytesIO(response.content))
            aspect_ratio = original_image.width / original_image.height
            
            if frame_width / frame_height > aspect_ratio:
                new_height = frame_height
                new_width = int(frame_height * aspect_ratio)
            else:
                new_width = frame_width
                new_height = int(frame_width / aspect_ratio)
            
            resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(resized_image)
            
            label_logo.configure(image=self.logo)
        except Exception as e:
            print(f"Error al actualizar la imagen: {e}")

    def toggle_panel(self, mostrar=None):
        if not hasattr(self, 'menu_lateral') or self.menu_lateral is None:
            return
            
        if mostrar is None:
            mostrar = not self.menu_lateral.winfo_ismapped()
        
        if mostrar:
            self.menu_lateral.grid(row=0, column=0, sticky="nsew")
        else:
            self.menu_lateral.grid_remove()

    def create_circular_image(self, image):
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, image.size[0], image.size[1]), fill=255)
        
        output = Image.new("RGBA", image.size, (0, 0, 0, 0))
        output.paste(image, (0, 0))
        output.putalpha(mask)
        
        return output

    def abrir_pantalla(self, funcion_pantalla):
        try:
            for widget in self.cuerpo_principal.winfo_children():
                widget.destroy()
            
            self.toggle_panel(False)
            funcion_pantalla(self.cuerpo_principal, self.cargar_pantalla_principal)
        except Exception as e:
            print(f"Error al abrir la pantalla: {e}")

if __name__ == "__main__":
    app = FormularioMaestroDesign()
    app.mainloop()