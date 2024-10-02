from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.widget import Widget
from Math.CalcularSugerencia import calcularSugerencia

Builder.load_file("pages/ConfirmData/ConfirmData.kv")

class ConfirmData(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.datosElejidos = []
    
    def loadData(self):
        selector = self.ids.selector_columna_datos
        app = App.get_running_app()
        for column in app.storage.datos:
            selector.values.append(column['columnName'])
    pass

    def selectDatos(self, opcion:str):
        label = self.ids.label_datos_vista_previa
        app = App.get_running_app()
        datos:list[dict] = app.storage.datos
        textoNuevo = "estos son los datos cargados:\n"
        for i in range(len(datos)):
            if datos[i]['columnName'] == opcion:
                
                if self.todosNumericos(datos[i]['values']):
                    self.ids.label_tipo_datos.text = "tipo de datos: cuantitativos"
                    app.storage.setTipoDatos("cuantitativos")
                else:
                    self.ids.label_tipo_datos.text = "tipo de datos: cualitativos"
                    app.storage.setTipoDatos("cualitativos")
                recorteDatos = 30 if len(datos[i]['values']) > 30 else len(datos[i]['values'])
                puntosRecorte = "..."if len(datos[i]['values']) > 30 else ""
                values_to_display = datos[i]['values'][:recorteDatos]
                for j in range(recorteDatos):
                    textoNuevo += f"{values_to_display[j]}, "
                textoNuevo += puntosRecorte
                break
        label.text = textoNuevo
        self.mostrarBotones()
        pass
    
    def todosNumericos(self,array):
        return all(isinstance(item, (int, float)) for item in array)
    
    def mostrarBotones(self):
        app = App.get_running_app()
        columna = self.ids.selector_columna_datos.text
        datos = []
        datos = next((c['values'] for c in app.storage.datos if c['columnName'] == columna), [])
        self.datosElejidos = datos
        if not self.todosNumericos(datos):
            self.ids.boton_distribucion_directa.center_x = self.width / 2
            return
        if calcularSugerencia(datos):
            self.ids.label_consejo_distribucion.center_x = self.width / 2
            self.ids.label_consejo_distribucion.text = ("se ha detectado una gran cantidad de datos demasiado dispersos, en total " 
            + f"{len(datos)} datos y la diferencia entre el mayor y el menor de ellos es de {max(datos)} a {min(datos)}")
            self.ids.boton_distribucion_directa.center_x = self.width / 4
            self.ids.boton_distribucion_agrupada.center_x = self.width * 3 / 4
        else:
            self.ids.label_consejo_distribucion.center_x = self.width * 2
            self.ids.boton_distribucion_agrupada.center_x = self.width * 2
            self.ids.boton_distribucion_directa.center_x = self.width / 2
        pass
    
    def siguientePagina(self,opcion:int):
        app = App.get_running_app()
        app.storage.datosElejidos = self.datosElejidos
        if opcion == 1:
            app.storage.setTipoTabla("directa")
        elif opcion == 2:
            app.storage.setTipoTabla("agrupada")
        app.root.current = 'tabla'
        pass

class ConfirmDataScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(ConfirmData())
        
    def on_enter(self):
        widget = self.children[0]
        widget.loadData()
        pass