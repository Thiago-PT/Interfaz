# form_iniciar_secion.py

import customtkinter as ctk
import pymysql
from tkinter import messagebox

# Definición de colores modernos
COLOR_PRINCIPAL = "#1a1b26"     # Azul oscuro
COLOR_SECUNDARIO = "#f0f5ff"    # Azul claro 
COLOR_ACENTO = "#2d4f7c"        # Azul medio
COLOR_HOVER = "#1a365d"         # Azul oscuro para hover
COLOR_CUERPO_PRINCIPAL = COLOR_SECUNDARIO  # Mismo color de fondo que form_tomar_datos.py

def iniciar_sesion():
    email_docente = usuario_entry.get()
    contrasena = contrasena_entry.get()

    try:
        # Establecer la conexión a la base de datos
        conn = pymysql.connect(host='b4qhbwwqys2nhher1vul-mysql.services.clever-cloud.com', port=3306, db='b4qhbwwqys2nhher1vul', user='upvge9afjesbmmgv', password='BS2bxJNACO1XYEmWBqA0')

        # Crear un objeto cursor
        cur = conn.cursor()

        # Preparar la consulta SQL para verificar los datos de inicio de sesión
        sql = "SELECT * FROM usuario WHERE correo = %s AND password = %s"

        # Ejecutar la consulta SQL con los valores obtenidos de los campos de entrada
        cur.execute(sql, (email_docente, contrasena))

        # Obtener el resultado de la consulta
        resultado = cur.fetchone()

        # Verificar si se obtuvo algún resultado
        if resultado:
            messagebox.showinfo("Inicio de Sesión", "Sesión iniciada exitosamente.")
        else:
            messagebox.showerror("Error", "Correo electrónico o contraseña incorrectos.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        # Cerrar la conexión a la base de datos
        if conn.open:
            cur.close()
            conn.close()

def mostrar_ventana_inicio_sesion(parent_frame, regresar_callback):
    # Limpiar frame principal
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Estilos y fuentes
    fuente_titulo = ("Roboto", 24, "bold")
    fuente_normal = ("Roboto", 14)

    # Frame principal
    main_frame = ctk.CTkFrame(parent_frame, fg_color=COLOR_CUERPO_PRINCIPAL)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Título
    titulo = ctk.CTkLabel(main_frame, text="Iniciar Sesión", font=fuente_titulo, text_color=COLOR_PRINCIPAL)
    titulo.pack(pady=20)

    # Campo de usuario
    usuario_label = ctk.CTkLabel(main_frame, text="Usuario:", font=fuente_normal, text_color=COLOR_PRINCIPAL)
    usuario_label.pack(pady=5)

    global usuario_entry
    usuario_entry = ctk.CTkEntry(main_frame, font=fuente_normal, height=45, width=300)
    usuario_entry.pack(pady=5)

    # Campo de contraseña
    contrasena_label = ctk.CTkLabel(main_frame, text="Contraseña:", font=fuente_normal, text_color=COLOR_PRINCIPAL)
    contrasena_label.pack(pady=5)

    global contrasena_entry
    contrasena_entry = ctk.CTkEntry(main_frame, show="*", font=fuente_normal, height=45, width=300)
    contrasena_entry.pack(pady=5)

    # Botón de inicio de sesión moderno
    boton_iniciar_sesion = ctk.CTkButton(
        main_frame, 
        text="Iniciar Sesión",
        command=iniciar_sesion,
        width=200,
        height=40,
        corner_radius=10,
        hover_color=COLOR_HOVER
    )
    boton_iniciar_sesion.pack(pady=10)

    # Botón para regresar moderno 
    boton_regresar = ctk.CTkButton(
        main_frame,
        text="Regresar",
        command=regresar_callback,
        width=200,
        height=40,
        corner_radius=10,
        hover_color=COLOR_HOVER
    )
    boton_regresar.pack(pady=10)