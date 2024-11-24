import os
import shutil
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import subprocess  # Para ejecutar comandos en la terminal

class DesinstaladorApp:
    def __init__(self, root):
        self.root = root
        self.root.resizable(False, False)
        
        # Inicialización de textos e idioma
        self.idioma_actual = "es"
        self.textos = {
            "es": {
                "titulo": "Desinstalador de League of Legends",
                "listo": "Listo",
                "buscar": "Buscar",
                "eliminar": "Eliminar",
                "buscando": "Buscando...",
                "ubicacion_encontrada": "Ubicación encontrada",
                "no_encontrado": "No encontrado",
                "desinstalacion_completada": "Desinstalación completada"
            },
            "en": {
                "titulo": "League of Legends Uninstaller",
                "listo": "Ready",
                "buscar": "Search",
                "eliminar": "Delete",
                "buscando": "Searching...",
                "ubicacion_encontrada": "Location found",
                "no_encontrado": "Not found",
                "desinstalacion_completada": "Uninstallation completed"
            }
        }[self.idioma_actual]

        # Estilo ttkbootstrap
        style = ttk.Style(theme="superhero")
        self.style = style

        # Título
        self.label_titulo = ttk.Label(root, text=self.textos["titulo"], font=("Helvetica", 18, "bold"))
        self.label_titulo.pack(pady=20)

        # Barra de progreso
        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, mode="determinate", length=500, bootstyle="info")
        self.progress.pack(pady=20)

        # Estado
        self.label_status = ttk.Label(root, text=self.textos["listo"], font=("Helvetica", 12), bootstyle="secondary")
        self.label_status.pack(pady=10)

        # Botón de Buscar
        self.boton_buscar = ttk.Button(root, text=self.textos["buscar"], bootstyle="primary", command=self.iniciar_busqueda)
        self.boton_buscar.pack(pady=5)

        # Botón de Eliminar (inicialmente deshabilitado)
        self.boton_eliminar = ttk.Button(root, text=self.textos["eliminar"], bootstyle="danger", state=tk.DISABLED, command=self.iniciar_eliminacion)
        self.boton_eliminar.pack(pady=5)

        # Botón de idioma (la bolita para cambiar de idioma)
        self.boton_idioma = ttk.Button(root, text="🌍", bootstyle="light", command=self.cambiar_idioma, width=3)
        self.boton_idioma.pack(pady=20)

    def iniciar_busqueda(self):
        self.progress["value"] = 0
        self.boton_buscar.config(state=tk.DISABLED)
        self.label_status.config(text=self.textos["buscando"])
        threading.Thread(target=self.proceso_busqueda).start()

    def proceso_busqueda(self):
        self.rutas_encontradas = buscar_en_linux("League of Legends", self.actualizar_progreso)
        if self.rutas_encontradas:
            self.label_status.config(text=self.textos["ubicacion_encontrada"])
            self.boton_buscar.pack_forget()
            self.boton_eliminar.config(state=tk.NORMAL)
            self.boton_eliminar.pack(pady=5)
        else:
            self.label_status.config(text=self.textos["no_encontrado"])
            self.boton_buscar.config(state=tk.NORMAL)

    def iniciar_eliminacion(self):
        self.progress["value"] = 0
        self.boton_eliminar.config(state=tk.DISABLED)
        self.label_status.config(text=self.textos["buscando"])
        threading.Thread(target=self.proceso_eliminacion).start()

    def proceso_eliminacion(self):
        eliminar_rutas(self.rutas_encontradas, self.actualizar_progreso)
        self.label_status.config(text=self.textos["desinstalacion_completada"])
        messagebox.showinfo(self.textos["titulo"], self.textos["desinstalacion_completada"])

    def actualizar_progreso(self, porcentaje):
        self.progress["value"] = porcentaje
        self.root.update_idletasks()

    def cambiar_idioma(self):
        if self.idioma_actual == "es":
            self.idioma_actual = "en"
        else:
            self.idioma_actual = "es"

        self.textos = {
            "es": {
                "titulo": "Desinstalador de League of Legends",
                "listo": "Listo",
                "buscar": "Buscar",
                "eliminar": "Eliminar",
                "buscando": "Buscando...",
                "ubicacion_encontrada": "Ubicación encontrada",
                "no_encontrado": "No encontrado",
                "desinstalacion_completada": "Desinstalación completada"
            },
            "en": {
                "titulo": "League of Legends Uninstaller",
                "listo": "Ready",
                "buscar": "Search",
                "eliminar": "Delete",
                "buscando": "Searching...",
                "ubicacion_encontrada": "Location found",
                "no_encontrado": "Not found",
                "desinstalacion_completada": "Uninstallation completed"
            }
        }[self.idioma_actual]

        self.label_titulo.config(text=self.textos["titulo"])
        self.label_status.config(text=self.textos["listo"])
        self.boton_buscar.config(text=self.textos["buscar"])
        self.boton_eliminar.config(text=self.textos["eliminar"])
        self.boton_idioma.config(text="🌍" if self.idioma_actual == "es" else "🌎")

def buscar_en_linux(nombre, callback):
    import time
    rutas = []
    posibles_rutas = [
        "/opt/leagueoflegends",
        "/usr/local/share/leagueoflegends",
        os.path.expanduser("~/League of Legends")
    ]
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            rutas.append(ruta)
            callback(100)
            break
    return rutas

def eliminar_rutas(rutas, callback):
    import time
    for ruta in rutas:
        if os.path.exists(ruta):
            try:
                subprocess.run(["rm", "-rf", ruta], check=True)
                callback(100)
            except subprocess.CalledProcessError:
                print(f"Error al eliminar {ruta}")
    return

if __name__ == "__main__":
    root = tk.Tk()
    app = DesinstaladorApp(root)
    root.mainloop()
