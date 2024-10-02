def calcularSugerencia(array: list) -> bool:
    if len(array) <= 10:
        return False
    if calcularDiversidad(array):
        return False
    decimales = calcularDecimales(array)
    mayor = max(array)
    menor = min(array)

    if decimales > 0:
        diferencia = 10 * (1/decimales)
    else:
        diferencia = 10

    return (mayor - menor) > diferencia

def calcularDecimales(array: list):
    decimales = 0
    for num in array:
        num_str = str(num)
        if '.' in num_str:
            num_decimales = len(num_str.split('.')[1])
            if num_decimales > decimales:
                decimales = num_decimales
    return 10 ** decimales

def calcularDiversidad(array: list):
    return len(set(array)) <= 10 # los sets no admiten duplicados, esto calcula que realmente hayan mas de 10 datos distintos en el dataset