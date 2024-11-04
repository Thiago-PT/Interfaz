# form_panel_datos.py

import customtkinter as ctk
from PIL import Image, ImageTk
import pymysql
from datetime import datetime
import csv
from typing import List, Tuple, Optional
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DatabaseConnection:
    def __init__(self):
        self.connection_params = {
            'host': 'b4qhbwwqys2nhher1vul-mysql.services.clever-cloud.com',
            'port': 3306,
            'db': 'b4qhbwwqys2nhher1vul',
            'user': 'upvge9afjesbmmgv',
            'password': 'BS2bxJNACO1XYEmWBqA0'
        }
        
    def __enter__(self):
        self.connection = self.get_connection()
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
    
    def get_connection(self) -> Optional[pymysql.Connection]:
        try:
            return pymysql.connect(**self.connection_params)
        except Exception as e:
            logging.error(f"Error de conexión a la base de datos: {e}")
            return None

class DataManager:
    @staticmethod
    def fetch_asistencia(limit: int = 100) -> List[Tuple]:
        with DatabaseConnection() as conn:
            if not conn:
                return []
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id, nombre, fecha, estado 
                        FROM asistencia 
                        ORDER BY fecha DESC 
                        LIMIT %s
                    """, (limit,))
                    return cursor.fetchall()
            except Exception as e:
                logging.error(f"Error al obtener datos de asistencia: {e}")
                return []

    @staticmethod
    def fetch_estudiantes() -> List[Tuple]:
        with DatabaseConnection() as conn:
            if not conn:
                return []
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM estudiantes")
                    return cursor.fetchall()
            except Exception as e:
                logging.error(f"Error al obtener estudiantes: {e}")
                return []

    @staticmethod
    def fetch_usuarios() -> List[Tuple]:
        with DatabaseConnection() as conn:
            if not conn:
                return []
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM usuario")
                    return cursor.fetchall()
            except Exception as e:
                logging.error(f"Error al obtener usuarios: {e}")
                return []

    @staticmethod
    def export_to_csv(datos: List[Tuple], filename: Optional[str] = None) -> str:
        if not filename:
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"exportacion_asistencia_{fecha_actual}.csv"
        
        try:
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Nombre", "Fecha", "Estado"])
                writer.writerows(datos)
            logging.info(f"Datos exportados exitosamente a {filename}")
            return filename
        except Exception as e:
            logging.error(f"Error al exportar datos: {e}")
            raise

class DashboardPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # Sección de Estadísticas
        self.create_stats_section()
        
        # Sección de Tabla de Asistencia
        self.create_attendance_table()
        
        # Botones de Control
        self.create_control_buttons()
        
    def create_stats_section(self):
        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        # Obtener datos para estadísticas
        estudiantes = DataManager.fetch_estudiantes()
        usuarios = DataManager.fetch_usuarios()
        asistencia = DataManager.fetch_asistencia()
        
        # Crear tarjetas de estadísticas
        self.create_stat_card(stats_frame, "Total Estudiantes", len(estudiantes), 0)
        self.create_stat_card(stats_frame, "Usuarios Activos", len(usuarios), 1)
        self.create_stat_card(stats_frame, "Asistencias Hoy", 
                            self.count_today_attendance(asistencia), 2)
        
    def create_stat_card(self, parent, title: str, value: int, column: int):
        card = ctk.CTkFrame(parent)
        card.grid(row=0, column=column, padx=10, pady=5, sticky="nsew")
        
        ctk.CTkLabel(card, text=title, font=("Roboto", 12)).pack(pady=5)
        ctk.CTkLabel(card, text=str(value), font=("Roboto", 20, "bold")).pack(pady=5)
        
    def count_today_attendance(self, asistencia: List[Tuple]) -> int:
        today = datetime.now().date()
        return sum(1 for a in asistencia if isinstance(a[2], datetime) 
                  and a[2].date() == today)
        
    def create_attendance_table(self):
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Encabezados
        columns = ["ID", "Nombre", "Fecha", "Estado"]
        for i, col in enumerate(columns):
            ctk.CTkLabel(
                self.table_frame,
                text=col,
                font=("Roboto", 12, "bold")
            ).grid(row=0, column=i, padx=5, pady=5, sticky="w")
            
        self.actualizar_tabla()
        
    def actualizar_tabla(self):
        # Limpiar tabla existente (excepto encabezados)
        for widget in self.table_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()
                
        # Obtener datos frescos
        datos = DataManager.fetch_asistencia()
        
        # Llenar tabla
        for i, row in enumerate(datos, start=1):
            for j, value in enumerate(row):
                if isinstance(value, datetime):
                    value = value.strftime("%Y-%m-%d %H:%M")
                    
                ctk.CTkLabel(
                    self.table_frame,
                    text=str(value),
                    font=("Roboto", 12)
                ).grid(row=i, column=j, padx=5, pady=2, sticky="w")
                
    def create_control_buttons(self):
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="Actualizar Datos",
            command=self.actualizar_tabla,
            width=150
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Exportar a CSV",
            command=self.exportar_datos,
            width=150
        ).pack(side="left", padx=5)
        
    def exportar_datos(self):
        datos = DataManager.fetch_asistencia()
        if datos:
            try:
                filename = DataManager.export_to_csv(datos)
                self.show_message(f"Datos exportados a {filename}")
            except Exception as e:
                self.show_message(f"Error al exportar: {str(e)}", "error")
                
    def show_message(self, message: str, msg_type: str = "info"):
        color = "red" if msg_type == "error" else "green"
        label = ctk.CTkLabel(
            self,
            text=message,
            text_color=color,
            font=("Roboto", 12)
        )
        label.pack(pady=5)
        self.after(3000, label.destroy)

def mostrar_panel_datos(frame_principal: ctk.CTkFrame, callback_return):
    # Limpiar frame principal
    for widget in frame_principal.winfo_children():
        widget.destroy()
        
    # Crear y mostrar el dashboard
    dashboard = DashboardPanel(frame_principal)
    dashboard.pack(fill="both", expand=True)
    
    # Botón para volver
    ctk.CTkButton(
        frame_principal,
        text="Volver al Menú Principal",
        command=lambda: callback_return(frame_principal),
        width=200
    ).pack(pady=10)

