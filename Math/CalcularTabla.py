import numpy as np
from Math.CalcularSugerencia import calcularDecimales

def calcularRango(array:list):
    return max(array) - min(array)

def calcularCantidadClases(array:list):
    num_clases = 1 + (3.3 * np.log10(len(array)))
    return int(np.ceil(num_clases))

def calcularAnchoClases(array:list):
    rango = calcularRango(array)
    num_clases = calcularCantidadClases(array)
    todos_enteros = all(isinstance(numero, int) for numero in array)
    ancho_de_clase_bruto = rango / num_clases
    return np.ceil(ancho_de_clase_bruto) if todos_enteros else ancho_de_clase_bruto

class Limite:
    def __init__(self, limite_inferior, limite_superior) -> None:
        self.limite_inferior = limite_inferior
        self.limite_superior = limite_superior

def calcularLimites(array:list) -> list[Limite]:
    decimales = calcularDecimales(array) if calcularDecimales(array) != 0 else 1
    decimales_extendidos = decimales * 10
    separador_de_limites = 1 / (decimales * 10)
    separador_de_limites *= 5 # aqui se calcula el .5 o 5 adicional para dividir el campo que abarca cada clase
    limites:list[Limite] = []
    ancho_clases = calcularAnchoClases(array)
    ancho_clases = (round(ancho_clases * decimales) / decimales)
    num_clases = calcularCantidadClases(array)
    limites.append(Limite(min(array), round((min(array) + ancho_clases + separador_de_limites) * decimales_extendidos) / decimales_extendidos))
    for i in range(num_clases - 1):
        limites.append(Limite(limites[i].limite_superior, round((limites[i].limite_superior + ancho_clases) * decimales_extendidos) / decimales_extendidos))
    return limites

def calcularMarcasDeClase(array:list):
    limites = calcularLimites(array)
    decimales = calcularDecimales(array)
    marcas_de_clases = []
    for limite in limites:
        marca = (limite.limite_superior + limite.limite_inferior) / 2
        marcas_de_clases.append(marca)
    if decimales != 0:
        marcas_de_clases = [(round(marca * decimales) / decimales) for marca in marcas_de_clases]
    return marcas_de_clases