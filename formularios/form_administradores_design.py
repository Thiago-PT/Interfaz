import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
import requests
from io import BytesIO
from formularios.form_Iniciar_Sesion import mostrar_ventana_inicio_sesion
from formularios.form_crear_cuenta import abrir_ventana_crear_cuenta
from formularios.form_tomar_datos import abrir_ventana_toma_de_datos
from formularios.form_panel_datos import mostrar_panel_datos
from formularios.form_salir import salir_aplicacion

# Definición de colores modernos
COLOR_BARRA_SUPERIOR = "#1a1b26"    # Azul oscuro
COLOR_MENU_LATERAL = "#2d4f7c"      # Azul medio
COLOR_CUERPO_PRINCIPAL = "#f0f5ff"  # Azul claro
COLOR_HOVER = "#1a365d"             # Azul oscuro para hover

class DriveImageLoader:
    """Clase para manejar la carga de imágenes desde Google Drive"""
    _cache = {}  # Cache para almacenar las imágenes originales

    @staticmethod
    def get_direct_download_url(sharing_url):
        """Convierte una URL de compartir de Google Drive en una URL de descarga directa"""
        file_id = sharing_url.split('/')[5]
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    
    @classmethod
    def load_image(cls, sharing_url):
        """Carga una imagen desde Google Drive y la almacena en caché"""
        try:
            # Verificar si la imagen está en caché
            if sharing_url in cls._cache:
                return cls._cache[sharing_url]

            direct_url = cls.get_direct_download_url(sharing_url)
            response = requests.get(direct_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            
            # Guardar en caché
            cls._cache[sharing_url] = image
            return image
        except Exception as e:
            print(f"Error al cargar la imagen desde Drive: {e}")
            return None

class FormularioAdministradorDesign(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # URLs de las imágenes en Drive
        self.URLS_IMAGENES = {
            'logo': "https://drive.google.com/file/d/19Ohw-T6nyFb3ENL0PLUQf2kI73C5eBPZ/view?usp=drive_link",
            'perfil': "https://drive.google.com/file/d/1D4OPybTHAjialmRe44ONqiip-TG4gY_c/view?usp=drive_link"
        }
        
        # Inicializar variables de instancia
        self.menu_lateral = None
        self.cuerpo_principal = None
        self.logo = None
        self.perfil = None
        self.logo_original = None  # Mantener referencia a la imagen original
        
        # Configurar tema
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        # Configurar ventana
        self.configurar_ventana()
        
        # Cargar imágenes
        self.loader = DriveImageLoader()
        self.cargar_imagenes()
        
        # Crear paneles
        self.crear_paneles()
        
        # Configurar controles
        self.configurar_controles()
        
        # Cargar pantalla principal
        self.cargar_pantalla_principal()

    def cargar_imagenes(self):
        """Carga todas las imágenes necesarias desde Google Drive"""
        try:
            # Cargar logo
            self.logo_original = self.loader.load_image(self.URLS_IMAGENES['logo'])
            if self.logo_original:
                self.logo = ImageTk.PhotoImage(self.logo_original)
            else:
                print("No se pudo cargar el logo")
                
            # Cargar imagen de perfil
            self.perfil_original = self.loader.load_image(self.URLS_IMAGENES['perfil'])
            if self.perfil_original:
                perfil_resized = self.perfil_original.resize((100, 100))
                perfil_circular = self.create_circular_image(perfil_resized)
                self.perfil = ImageTk.PhotoImage(perfil_circular)
            else:
                print("No se pudo cargar la imagen de perfil")
                
        except Exception as e:
            print(f"Error al cargar las imágenes: {e}")

    def configurar_ventana(self):
        self.title('Eye System - Administrador')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height-40}+0+0")
        self.resizable(True, True)

    def crear_paneles(self):
        # [El resto del método permanece igual]
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

    def configurar_menu_lateral(self):
        if hasattr(self, 'perfil') and self.perfil:
            label_perfil = ctk.CTkLabel(self.menu_lateral, image=self.perfil, text="")
            label_perfil.pack(pady=20)

        # Definir botones
        botones_info = [
            ("Iniciar Sesión", lambda: self.abrir_pantalla(mostrar_ventana_inicio_sesion)),
            ("Crear Cuenta", lambda: self.abrir_pantalla(abrir_ventana_crear_cuenta)),
            ("Tomar Datos", lambda: self.abrir_pantalla(abrir_ventana_toma_de_datos)),
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

    def actualizar_imagen(self, event, label_logo):
        try:
            frame_width = event.width
            frame_height = event.height
            
            if self.logo_original:
                aspect_ratio = self.logo_original.width / self.logo_original.height
                
                if frame_width / frame_height > aspect_ratio:
                    new_height = frame_height
                    new_width = int(frame_height * aspect_ratio)
                else:
                    new_width = frame_width
                    new_height = int(frame_width / aspect_ratio)
                
                resized_image = self.logo_original.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.logo = ImageTk.PhotoImage(resized_image)
                label_logo.configure(image=self.logo)
                
        except Exception as e:
            print(f"Error al actualizar la imagen: {e}")

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
        
        if self.logo_original:
            aspect_ratio = self.logo_original.width / self.logo_original.height
            
            if frame_width / frame_height > aspect_ratio:
                new_height = frame_height
                new_width = int(frame_height * aspect_ratio)
            else:
                new_width = frame_width
                new_height = int(frame_width / aspect_ratio)
            
            resized_image = self.logo_original.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(resized_image)
            
            label_logo = ctk.CTkLabel(frame_principal, image=self.logo, text="")
            label_logo.place(relx=0.5, rely=0.5, anchor='center')
            
            frame_principal.bind('<Configure>', lambda e: self.actualizar_imagen(e, label_logo))

    # Los métodos restantes permanecen igual
    def create_circular_image(self, image):
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, image.size[0], image.size[1]), fill=255)
        output = Image.new("RGBA", image.size, (0, 0, 0, 0))
        output.paste(image, (0, 0))
        output.putalpha(mask)
        return output

    def toggle_panel(self, mostrar=None):
        if mostrar is None:
            mostrar = not self.menu_lateral.winfo_ismapped()
        
        if mostrar:
            self.menu_lateral.grid(row=0, column=0, sticky="nsew")
        else:
            self.menu_lateral.grid_remove()

    def abrir_pantalla(self, funcion):
        funcion(self.cuerpo_principal, self.cargar_pantalla_principal)

    def configurar_controles(self):
        # Configurar barra superior
        self.label_titulo = ctk.CTkLabel(
            self.barra_superior,
            text="Eye System - Administrador",
            font=("Roboto", 20, "bold"),
            text_color="white"
        )
        self.label_titulo.pack(side='left', padx=20)
        
        # Botón de menú
        self.button_menu = ctk.CTkButton(
            self.barra_superior,
            text="≡",
            width=40,
            command=self.toggle_panel,
            fg_color="transparent",
            hover_color=COLOR_HOVER
        )
        self.button_menu.pack(side='left', padx=10)
        
        # Configurar menú lateral
        self.configurar_menu_lateral()

if __name__ == "__main__":
    app = FormularioAdministradorDesign()
    app.mainloop()