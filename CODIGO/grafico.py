#importar variables de codigo.py

#Dibujar las redes de flujo en python, las cuadriculas deben ser de 5x5 mm
#Abajo tiene que ser curvo
#Intentar hacer en autocad

from variables import caso_1, caso_2, caso_3, num_equipotenciales
from matplotlib import pyplot as plt
from lineas import agregar_linea_horizontal, agregar_linea_vertical
from lineas_flujo import agregar_red_de_flujo
from lineas_equipotenciales import agregar_lineas_equipotenciales, extraer_pendientes, extraer_puntos, graficar_lineas_con_pendientes


# Dimensiones de la hoja A4 en milímetros
ancho_a4_mm = 210
alto_a4_mm = 297

# Tamaño de la cuadrícula en milímetros
tamanio_cuadricula_mm = 5

def crear_hoja_cuadriculada(ancho, alto, tamanio_cuadricula):
    # Configurar la figura para que tenga el tamaño de una hoja A4 en pulgadas (1 pulgada = 25.4 mm)
    fig, ax = plt.subplots(figsize=(ancho / 25.4, alto / 25.4), dpi=100)
    
    # Eliminar márgenes
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    
    # Dibujar líneas verticales
    for x in range(0, ancho + tamanio_cuadricula, tamanio_cuadricula):
        ax.axvline(x, color='gray', linewidth=0.5)

    # Dibujar líneas horizontales
    for y in range(0, alto + tamanio_cuadricula, tamanio_cuadricula):
        ax.axhline(y, color='gray', linewidth=0.5)

    # Establecer los límites de la gráfica
    ax.set_xlim(0, ancho)
    ax.set_ylim(0, alto)

    # Eliminar marcas de los ejes
    ax.set_xticks([])
    ax.set_yticks([])

    return ax

def graficar(caso, nombre, altura_base):
    d = 20.0
    ax = crear_hoja_cuadriculada(ancho_a4_mm, alto_a4_mm, tamanio_cuadricula_mm)
    #agregar_linea_horizontal(ax, 0.5 + altura_base, 0, 210, 'black')  # Linea de fondo
    C1 = (caso['c1'] * 1000) / 200  # Convierto a escala 1:200
    agregar_linea_horizontal(ax, C1 + altura_base, 0, 105, 'black')  # Linea de C1
    C2 = (caso['c2'] * 1000) / 200  # Convierto a escala 1:200
    agregar_linea_horizontal(ax, C2 + altura_base, 105, 105, 'black')  # Linea de C2
    B1 = (caso['b1']*1000)/200 #Convierto a escala 1:200
    B1 = B1 + C1 #Sumo la altura de C1
    agregar_linea_horizontal(ax, B1+altura_base, 0, 105, 'blue') #Linea de B1
    B2 = (caso['b2']*1000)/200 #Convierto a escala 1:200
    B2 = B2 + C2 #Sumo la altura de C2
    agregar_linea_horizontal(ax, B2+altura_base, 105, 105, 'blue') #Linea de B2
    A1 = (caso['a1']*1000)/200 #Convierto a escala 1:200
    A1 = A1 + B1 #Sumo la altura de B1
    agregar_linea_vertical(ax, 105, C2+altura_base-d, A1+altura_base) #Linea de A1
    
    # Dibujar una curva de flujo con dos puntos de control
    punto_1 =(C2-d)/4
    punto_2 = punto_1*2
    punto_3 = punto_1*3
    bezier_path_1 = agregar_red_de_flujo(ax, (26.25, C1), (52.5,punto_1 ),(105, punto_1), (157.5, punto_1), (183.75, C2), altura_base)
    bezier_path_2 = agregar_red_de_flujo(ax, (26.25*2, C1), (65.625,punto_2 ), (105, punto_2), (144.375, punto_2),(183.75-26.25, C2), altura_base)
    bezier_path_3 = agregar_red_de_flujo(ax, (26.25*3, C1), (75.75,punto_3 ), (105, punto_3), (134.25, punto_3), (183.75-(26.25*2), C2), altura_base)

    bezier_path_4 = agregar_red_de_flujo(ax, (0, 0), (52.5, 0), (105, 0), (157.5, 0), (210, 0), altura_base)

    # Dibujar las líneas equipotenciales
    pendientes_1, coordenadas_1 = agregar_lineas_equipotenciales(ax, bezier_path_1, num_equipotenciales, longitud=10, color='green', grosor=1)
    pendientes_2, coordenadas_2 = agregar_lineas_equipotenciales(ax, bezier_path_2, num_equipotenciales, longitud=10, color='green', grosor=1)
    pendientes_3, coordenadas_3 = agregar_lineas_equipotenciales(ax, bezier_path_3, num_equipotenciales, longitud=10, color='green', grosor=1)
    pendientes_4, coordenadas_4 = agregar_lineas_equipotenciales(ax, bezier_path_4, num_equipotenciales, longitud=10, color='green', grosor=1)
    
    # Obtener las claves del diccionario
    claves = list(pendientes_4.keys())

    # Calcular el punto de la mitad
    mitad = len(claves) // 2

    # Asignar valores de +10 para la primera mitad
    for i in range(mitad):
        pendientes_4[claves[i]] = 10.0

    # Asignar valores de -10 para la segunda mitad
    for i in range(mitad, len(claves)):
        pendientes_4[claves[i]] = -10.0



    pendientes = [pendientes_4, pendientes_1, pendientes_2, pendientes_3]
    coordenadas = [coordenadas_4, coordenadas_1, coordenadas_2, coordenadas_3]

    # Llamar a la función para graficar las líneas
    graficar_lineas_con_pendientes(ax, coordenadas, pendientes, color='green', grosor=1)

    # Guardar la figura usando el objeto ax
    plt.savefig(f"{nombre}.pdf", format='pdf', bbox_inches='tight', pad_inches=0)

# Ejemplo de uso
graficar(caso_1, 'caso_1', 50)
graficar(caso_2, 'caso_2', 50)
graficar(caso_3, 'caso_3', 50)