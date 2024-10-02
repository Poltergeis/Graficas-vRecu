from Math.CalcularTabla import Limite

class DataStorage:
    def __init__(self) -> None:
        self.limites:list[Limite] = []
        self.frecuenciasRelativas:list = []
        self.frecuenciasAbsolutas:list = []
        self.indexTabla:int = None
        self.intervalo = []
        self.anchosClase = []
        self.marcasDeClase:list = []
        self._tipoTabla:int = None
        self._tipoDatos:str = None
        self.rango = None
        self.numeroDeClases:int = None
        self.mediana = None
        self.moda = None
        self.media = None
        self.varianza = None
        self.cargadoDesdeArchivo:bool = None
        self.datos = []
        self.datosElejidos = []
        self.cantidadClases = None
        self.selectedGrafica = None
        pass
    
    def setTipoTabla(self,tipoTabla:str):
        if tipoTabla.lower() == "directa" or tipoTabla.lower() == "agrupada":
            self._tipoTabla = tipoTabla.lower()
        else:
            raise ValueError("tipo de tabla incorrecto")
        
    def getTipoTabla(self) -> str:
        return self._tipoTabla
        
    def setTipoDatos(self, tipoDatos:str):
        if tipoDatos.lower() == "cualitativos" or tipoDatos.lower() == "cuantitativos":
            self._tipoDatos = tipoDatos.lower()
        else:
            raise ValueError("tipo de datos incorrecto")
        
    def getTipoDatos(self) -> str:
        return self._tipoDatos
    
    def clear(self):
        self.limites = []
        self.frecuenciasRelativas:list = []
        self.frecuenciasAbsolutas:list = []
        self.indexTabla:int = 0
        self.intervalo = 0
        self.marcasDeClase:list = []
        self._tipoTabla:int = 0
        self._tipoDatos:str = 0
        self.rango = 0
        self.numeroDeClases:int = 0
        self.mediana = 0
        self.moda = 0
        self.media = 0
        self.varianza = 0
        self.cargadoDesdeArchivo:bool = None
        self.datos = []
        self.datosElejidos = []
        self.cantidadClases = 0