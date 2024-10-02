from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.app import App

Builder.load_file("pages/vistaGrafica/VistaGrafica.kv")

class VistaGrafica(Widget):
    def load_grafica(self):
        app = App.get_running_app()
        if app.storage.selectedGrafica:
            grafica = app.storage.selectedGrafica()
            box_layout = self.ids.grafica_container
            box_layout.add_widget(grafica)
            
    def volver(self):
        app = App.get_running_app()
        app.storage.selectedGrafica = None
        box_layout = self.ids.grafica_container
        box_layout.clear_widgets()
        app.root.current = 'tabla'


class VistaGraficaScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(VistaGrafica())
        
    def on_enter(self):
        widget = self.children[0]
        widget.load_grafica()