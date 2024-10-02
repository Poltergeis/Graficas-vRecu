from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.app import App
from Math.CalcularSugerencia import calcularSugerencia


Builder.load_file("pages/AltConfirmData/AltConfirmData.kv")

class AltConfirmData(Widget):
    def load_data(self):
        app = App.get_running_app()
        datosElejidos = app.storage.datosElejidos
        if app.storage.getTipoDatos() == "cualitativos":
            print("aqui")
            app.root.current = 'tabla'
            return
        if not calcularSugerencia(datosElejidos):
            app.storage.setTipoTabla("directa")
            app.root.current = 'tabla'
            return
        label = self.ids.alt_label_resumen_datos
        label.text = (f"se han detectado datos muy dispersos, almenos {len(datosElejidos)} datos"
                 + f" con mas de 10 distintos y una rango de dispersion de {max(datosElejidos)} a {min(datosElejidos)}")
        pass
    
    def siguientePagina(self, opcion:int):
        app = App.get_running_app()
        if opcion == 1:
            app.storage.setTipoTabla("directa")
        elif opcion == 2:
            app.storage.setTipoTabla("agrupada")
        app.root.current = 'tabla'

class AltConfirmDataScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(AltConfirmData())
        
    def on_enter(self):
        widget = self.children[0]
        widget.load_data()
        pass