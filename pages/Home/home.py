from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.widget import Widget
import re
import pandas as pd
import tkinter as Tk
from tkinter import filedialog
import json

Builder.load_file("pages/Home/home.kv")

class Home(Widget):
    def cargarExcel(self):
        root = Tk.Tk() #usamos tkinter solo para la ventana de archivos
        root.withdraw()
        ruta_archivo = filedialog.askopenfilename(
            title="Selecciona un archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx *.xls")]  # Filtrar solo archivos Excel
        )
        self.procesarExcel(ruta_archivo)
        root.destroy()
        pass
    
    def cargarCSV(self):
        root = Tk.Tk()
        root.withdraw()
        ruta_archivo = filedialog.askopenfilename(
            title="Selecciona un archivo csv",
            filetypes=[("Archivos CSV", "*.csv")]  # Filtrar solo archivos Excel
        )
        self.procesarCSV(ruta_archivo)
        pass
    
    def cargarDatosManuales(self):
        values: str = self.ids.numeros_input.text
        values_array = values.split(',')
        values_array = [value.strip() for value in values_array]
        app = App.get_running_app()

        # Función para verificar si un valor es numérico
        def es_numero(val):
            try:
                float(val)  # Intenta convertir a float
                return True
            except ValueError:
                return False

        # Verificar si hay caracteres no numéricos en el array
        for value in values_array:
            if not es_numero(value):
                # Si encontramos caracteres no numéricos, guardar el array bruto
                app.storage.datosElejidos = values_array
                app.storage.setTipoDatos("cualitativos")
                app.storage.setTipoTabla("directa")
                app.root.current = 'tabla'
                return

        # Convertir todos los valores a números
        app.storage.setTipoDatos("cuantitativos")
        datos_convertidos = []
        hay_flotante = False

        for value in values_array:
            if '.' in value:  # Determina si es un flotante
                datos_convertidos.append(float(value))  # Agrega como flotante
                hay_flotante = True
            else:
                datos_convertidos.append(int(value))  # Agrega como entero

        # Si hay al menos un flotante, convertimos todos a flotantes
        if hay_flotante:
            datos_convertidos = [float(num) for num in datos_convertidos]

        # Almacenar el array convertido
        app.storage.datosElejidos = datos_convertidos

        app.root.current = 'altConfirmData'

    
    def checarInput(self, texto):
        patron = r"^(?:[^,\s]+,)*[^,\s]+$" # aqui invocamos al diablo para que el usuario ponga comas
        if texto.strip() and re.match(patron, texto) is not None:
            self.ids.boton_carga_manual.disabled = False
            self.ids.label_error_datos_manuales.center_x = self.width * 2 # lo mandamos fuera de la pantalla
        else:
            self.ids.boton_carga_manual.disabled = True
            self.ids.label_error_datos_manuales.center_x = self.width / 2 # lo traemos de vuelta
        pass
    
    def procesarExcel(self, rutaExcel):
        df = pd.read_excel(rutaExcel)
        columnas_array = []
        
        for idx,columna in enumerate(df.columns):
            valores_columna = df[columna].dropna().tolist()
            if valores_columna:
                columnas_array.append({ 'columnName': f'columna{idx+1}', 'values': valores_columna })
        app = App.get_running_app()
        app.storage.datos = columnas_array
        app.root.current = 'confirmData'
        
    def procesarCSV(self, rutaCSV):
        df = pd.read_csv(rutaCSV)
        columnas_array = []
        for idx, columna in enumerate(df.columns):
            valores_columna = df[columna].dropna().tolist()
            if valores_columna:
                columnas_array.append({ 'columnName': f'columna{idx+1}', 'values': valores_columna })
        app = App.get_running_app()
        app.storage.datos = columnas_array
        app.root.current = 'confirmData'
    
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Home())