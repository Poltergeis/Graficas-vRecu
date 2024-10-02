from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from pages.Home.home import HomeScreen
from utils.DataStorage import DataStorage
from pages.ConfirmData.ConfirmData import ConfirmDataScreen
from pages.AltConfirmData.AltConfirmData import AltConfirmDataScreen
from pages.TablaFrecuencias.tablaFrecuencias import TablaFrecuenciasScreen
from pages.vistaGrafica.VistaGrafica import VistaGraficaScreen

Builder.load_file("app.kv")

class GraphicApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ConfirmDataScreen(name='confirmData'))
        sm.add_widget(AltConfirmDataScreen(name='altConfirmData'))
        sm.add_widget(TablaFrecuenciasScreen(name='tabla'))
        sm.add_widget(VistaGraficaScreen(name='grafica'))
        return sm
    
    def on_start(self):
        self.storage = DataStorage()
    
    
if __name__ == "__main__":
    GraphicApp().run()