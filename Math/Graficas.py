import matplotlib.pyplot as plt
import numpy as np
from kivy.uix.image import Image
from kivy.graphics.texture import Texture

def fig_to_texture(fig):
    """Convertir una figura de matplotlib en una textura de Kivy"""
    fig.canvas.draw()
    width, height = fig.canvas.get_width_height()
    buf = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8).reshape(height, width, 3)
    
    texture = Texture.create(size=(width, height))
    texture.blit_buffer(buf.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
    texture.flip_vertical()
    
    return texture

def mostrarOjiva(frecRels):
    """Crear un gráfico de ojiva"""
    datos_ordenados = sorted(frecRels)
    freq_acumulada = np.cumsum(frecRels) / np.sum(frecRels)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(datos_ordenados, freq_acumulada, marker='o')
    ax.fill_between(datos_ordenados, freq_acumulada, alpha=0.3)
    
    ax.set_title('Gráfico de Ojiva')
    ax.set_xlabel('Valores')
    ax.set_ylabel('Frecuencia Acumulada Relativa')
    ax.set_ylim(0, 1.05)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    ax.annotate('Mediana', xy=(np.median(datos_ordenados), 0.5), xytext=(np.median(datos_ordenados), 0.6),
                arrowprops=dict(facecolor='black', shrink=0.05))
    
    ax.text(0.95, 0.05, f'Total de datos: {len(frecRels)}\nMínimo: {min(frecRels)}\nMáximo: {max(frecRels)}', 
            transform=ax.transAxes, verticalalignment='bottom', 
            horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    texture = fig_to_texture(fig)
    return Image(texture=texture)

def mostrarPolFrec(frecAbs, marcas_clase, ancho_clase):
    """Crear un polígono de frecuencias"""
    x_extendido = [marcas_clase[0] - ancho_clase] + marcas_clase + [marcas_clase[-1] + ancho_clase]
    y_extendido = [0] + frecAbs + [0]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(x_extendido, y_extendido, marker='o', linestyle='-')
    ax.fill(x_extendido, y_extendido, alpha=0.3)
    
    ax.set_title('Polígono de Frecuencias')
    ax.set_xlabel('Marcas de Clase')
    ax.set_ylabel('Frecuencia')
    ax.set_xticks(marcas_clase)
    ax.set_xticklabels(marcas_clase, rotation=45, ha='right')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    max_freq_index = frecAbs.index(max(frecAbs))
    ax.annotate('Frecuencia máxima', 
                xy=(marcas_clase[max_freq_index], max(frecAbs)),
                xytext=(marcas_clase[max_freq_index] + ancho_clase, max(frecAbs) + 1),
                arrowprops=dict(facecolor='black', shrink=0.05))
    
    ax.text(0.95, 0.95, f'Total de datos: {sum(frecAbs)}\n'
                        f'Ancho de clase: {ancho_clase}\n'
                        f'Rango: {marcas_clase[-1] - marcas_clase[0] + ancho_clase}', 
            transform=ax.transAxes, verticalalignment='top', 
            horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    texture = fig_to_texture(fig)
    return Image(texture=texture)

def mostrarHist(marcas_clase, frecAbs, ancho_clase):
    """Crear un histograma"""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(marcas_clase, frecAbs, width=ancho_clase, align='center', edgecolor='black')
    
    ax.set_title('Histograma')
    ax.set_xlabel('Marcas de Clase')
    ax.set_ylabel('Frecuencia Absoluta')
    ax.set_xticks(marcas_clase)
    ax.set_xticklabels(marcas_clase, rotation=45, ha='right')
    
    max_freq_index = frecAbs.index(max(frecAbs))
    ax.annotate('Pico del histograma', 
                xy=(marcas_clase[max_freq_index], max(frecAbs)),
                xytext=(marcas_clase[max_freq_index] + 1, max(frecAbs) + 1),
                arrowprops=dict(facecolor='black', shrink=0.05))
    
    ax.text(0.95, 0.95, f'Total de datos: {sum(frecAbs)}', 
            transform=ax.transAxes, verticalalignment='top', 
            horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    texture = fig_to_texture(fig)
    return Image(texture=texture)

def mostrarCircular(datos):
    """Crear un gráfico circular"""
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(datos, labels=[f'Clase {i+1}' for i in range(len(datos))], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    ax.set_title('Gráfico Circular')
    
    texture = fig_to_texture(fig)
    return Image(texture=texture)