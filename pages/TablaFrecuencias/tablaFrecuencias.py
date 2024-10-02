from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.app import App
from Math.CalcularTabla import (calcularRango, calcularCantidadClases, calcularAnchoClases, calcularLimites, calcularMarcasDeClase, 
                                calcularDecimales, Limite)
from kivymd.uix.datatables import MDDataTable
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from Math.Graficas import mostrarCircular, mostrarHist, mostrarOjiva, mostrarPolFrec

Builder.load_file("pages/TablaFrecuencias/tablaFrecuencias.kv")

class TablaFrecuencias(Widget):
    def load_data(self):
        label = self.ids.label_tabla_titulo
        app = App.get_running_app()
        label.text = ('tabla de frecuencias ' + app.storage.getTipoTabla() + ' para datos de tipo ' + app.storage.getTipoDatos())
        
        atributos_tabla = []
        
        if app.storage.getTipoDatos() == "cualitativos":
            self.ids.boton_mostrar_ojiva.center_x = self.width * 2
            self.ids.boton_mostrar_polFrec.center_x = self.width * 2
            self.ids.boton_mostrar_histograma.center_x = self.center_x * 0.65
            self.ids.boton_mostrar_circular.center_x = self.center_x * 1.15
        
        if app.storage.getTipoTabla() == "directa":
            atributos_tabla = ['index', 'valor', 'frecuencia absoluta', 'frecuencia relativa']
            datosElejidos = app.storage.datosElejidos
            datosElejidosSinRepetidos = set(sorted(datosElejidos)) #if all(isinstance(dato, (int,float)) for dato in datosElejidos) else set(datosElejidos)
            datosElejidosSinRepetidos = list(datosElejidosSinRepetidos)
            decimales = calcularDecimales(datosElejidosSinRepetidos) if all(isinstance(dato, (float)) for dato in datosElejidosSinRepetidos) else 10 ** 3
            index = len(datosElejidosSinRepetidos)
            frecAbs = [datosElejidos.count(dato) for dato in datosElejidosSinRepetidos]
            app.storage.frecuenciasAbsolutas = frecAbs
            frecRel = [(round((dato / len(datosElejidos)) * decimales)) / decimales for dato in frecAbs]
            app.storage.frecuenciasRelativas = frecRel
            datos_brutos = [(str(i+1), str(datosElejidosSinRepetidos[i]), str(frecAbs[i]), str(frecRel[i])) for i in range(index)]
            print("---------------------------------------")
            print(datos_brutos)
            tabla_height = dp(50) * (len(datos_brutos) + 1)
            tabla = MDDataTable(
                size_hint_y = None,
                height = tabla_height,
                column_data = [(atributo, dp(43)) for atributo in atributos_tabla],
                row_data = datos_brutos,
                use_pagination = False,
                rows_num = index
            )
            scroll_view = ScrollView(size_hint=(1, None), size=(1340, 600), pos=(int(self.width * 0.15), int(self.top * 0.25)))
            scroll_view.add_widget(tabla)
            self.add_widget(scroll_view)
        else:
            atributos_tabla = ['clase', 'limite inferior', 'limite superior', 'marca de clase', 'frecuencia absoluta', 'frecuencia relativa', 'frecuencia absoluta acumulada']
            datosElejidos = app.storage.datosElejidos
            datosElejidosSinRepetidos = set(sorted(datosElejidos))
            datosElejidosSinRepetidos = list(datosElejidosSinRepetidos)
            limites:list[Limite] = calcularLimites(datosElejidos)
            marcas_de_clase = calcularMarcasDeClase(datosElejidos)
            app.storage.marcasDeClase = marcas_de_clase
            frecAbs = [sum(1 for idx, num in enumerate(datosElejidos) if limite.limite_inferior < num < limite.limite_superior) for limite in limites]
            frecAbs[0] = frecAbs[0] + datosElejidos.count(min(datosElejidos))
            app.storage.frecuenciasAbsolutas = frecAbs
            decimales = calcularDecimales(datosElejidosSinRepetidos) if all(isinstance(dato, (float)) for dato in datosElejidosSinRepetidos) else 10 ** 4
            frecRel = [(round((dato / len(datosElejidos)) * decimales)) / decimales for dato in frecAbs]
            app.storage.frecuenciasRelativas = frecRel
            frecAbsAcumulada = self.suma_acumulada(frecAbs)
            num_clases = calcularCantidadClases(datosElejidos)
            app.storage.anchosClase = calcularAnchoClases(datosElejidos)
            datos_brutos = [(i+1, limites[i].limite_inferior, limites[i].limite_superior, marcas_de_clase[i], frecAbs[i], frecRel[i], frecAbsAcumulada[i]) for i in range(num_clases)]
            print("---------------------------------------")
            print(datos_brutos)
            tabla_height = dp(50) * (len(datos_brutos) + 1)
            tabla = MDDataTable(
                size_hint_y = None,
                height = tabla_height,
                column_data = [(atributo, dp(25)) for atributo in atributos_tabla],
                row_data = datos_brutos,
                use_pagination = False,
                rows_num = num_clases
            )
            scroll_view = ScrollView(size_hint=(1, None), size=(1340, 600), pos=(int(self.width * 0.15), int(self.top * 0.25)))
            scroll_view.add_widget(tabla)
            self.add_widget(scroll_view)
            
    def suma_acumulada(self,arr):
        resultado = []
        suma = 0
        for num in arr:
            suma += num
            resultado.append(suma)
        return resultado
    
    def graficaCircular(self):
        app = App.get_running_app()
        app.storage.selectedGrafica = lambda: mostrarCircular(app.storage.datosElejidos)
        app.root.current = 'grafica'
        
    def histograma(self):
        app = App.get_running_app()
        app.storage.selectedGrafica = lambda: mostrarHist(app.storage.marcasDeClase, app.storage.frecuenciasAbsolutas, app.storage.marcasDeClase)
        app.root.current = 'grafica'
        
    def graficaPolFrec(self):
        app = App.get_running_app()
        app.storage.selectedGrafica = lambda: mostrarPolFrec(app.storage.frecuenciasAbsolutas, app.storage.marcasDeClase, app.storage.anchosClase)
        app.root.current = 'grafica'
        
    def ojiva(self):
        app = App.get_running_app()
        app.storage.selectedTabla = lambda: mostrarOjiva(app.storage.frecuenciasRelativas)
        app.root.current = 'grafica'
            
class TablaFrecuenciasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(TablaFrecuencias())
        
    def on_enter(self):
        widget = self.children[0]
        widget.load_data()