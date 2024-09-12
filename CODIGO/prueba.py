import numpy as np

import numpy as np

def agregar_lineas_equipotenciales(ax, bezier_path, num_equipotenciales=5, longitud=10, color='green', grosor=1):

    # Diccionario para almacenar la pendiente en cada punto y coordenadas
    pendientes_diccionario = {}
    coordenadas_diccionario = {}

    # Calcular la longitud total de la curva y obtener el centro
    longitud_total = 0
    longitudes_parciales = [0]  # Lista para almacenar la longitud acumulada
    for i in range(1, len(bezier_path)):
        dx = bezier_path[i][0] - bezier_path[i - 1][0]
        dy = bezier_path[i][1] - bezier_path[i - 1][1]
        distancia = np.sqrt(dx**2 + dy**2)
        longitud_total += distancia
        longitudes_parciales.append(longitud_total)

    # El punto central en términos de longitud total
    longitud_central = longitud_total / 2

    # Encontrar el índice donde la longitud acumulada se acerca al punto central
    for j in range(1, len(longitudes_parciales)):
        if longitudes_parciales[j] >= longitud_central:
            t = (longitud_central - longitudes_parciales[j - 1]) / (longitudes_parciales[j] - longitudes_parciales[j - 1])
            x_centro = bezier_path[j - 1][0] * (1 - t) + bezier_path[j][0] * t
            y_centro = bezier_path[j - 1][1] * (1 - t) + bezier_path[j][1] * t
            break
    
    # Coordenadas del punto central
    centro_curva = np.array([x_centro, y_centro])

    # Calcular la distancia de cada punto de la curva al centro
    distancias_al_centro = np.linalg.norm(bezier_path - centro_curva, axis=1)

    # Dividir la curva en puntos, concentrando más líneas equipotenciales cerca del centro
    indices_ordenados = np.argsort(distancias_al_centro)
    indices_equipotenciales = indices_ordenados[:num_equipotenciales]

    i = 0
    for idx in sorted(indices_equipotenciales):
        # Punto en la curva donde vamos a colocar la línea equipotencial
        x, y = bezier_path[idx]
        
        # Derivada numérica para calcular la pendiente de la curva en ese punto
        if idx > 0:
            dx = bezier_path[idx][0] - bezier_path[idx - 1][0]
            dy = bezier_path[idx][1] - bezier_path[idx - 1][1]
        else:
            # Si estamos en el primer punto, tomamos la derivada con el siguiente
            dx = bezier_path[idx + 1][0] - bezier_path[idx][0]
            dy = bezier_path[idx + 1][1] - bezier_path[idx][1]

        # Pendiente de la curva de flujo
        pendiente_flujo = dy / dx if dx != 0 else np.inf
        
        # Pendiente de la línea equipotencial, que es el negativo recíproco
        if pendiente_flujo != 0 and pendiente_flujo != np.inf:
            pendiente_equipotencial = -1 / pendiente_flujo
        elif pendiente_flujo == 0:
            pendiente_equipotencial = np.inf  # Línea equipotencial será vertical
        else:
            pendiente_equipotencial = 0  # Línea equipotencial será horizontal

        # Almacenar la pendiente en el diccionario
        pendientes_diccionario[f'punto_{i}'] = pendiente_equipotencial

        # Almacenar las coordenadas en el diccionario
        coordenadas_diccionario[f'punto_{i}'] = (x, y)
        
        # Calcular los puntos de la línea equipotencial
        if pendiente_equipotencial == np.inf:
            # Línea equipotencial vertical
            x_values = [x, x]
            y_values = [y - longitud / 2, y + longitud / 2]
        elif pendiente_equipotencial == 0:
            # Línea equipotencial horizontal
            x_values = [x - longitud / 2, x + longitud / 2]
            y_values = [y, y]
        else:
            # Caso general
            delta_x = longitud / (2 * np.sqrt(1 + pendiente_equipotencial**2))
            delta_y = pendiente_equipotencial * delta_x
            x_values = [x - delta_x, x + delta_x]
            y_values = [y - delta_y, y + delta_y]
        
        # Dibujar la línea equipotencial
        ax.plot(x_values, y_values, color=color, linewidth=grosor)
        i += 1

    return pendientes_diccionario, coordenadas_diccionario


#importar variables de codigo.py

#Dibujar las redes de flujo en python, las cuadriculas deben ser de 5x5 mm
#Abajo tiene que ser curvo
#Intentar hacer en autocad

from variables import caso_1, caso_2, caso_3, num_equipotenciales
from matplotlib import pyplot as plt
from lineas import agregar_linea_horizontal, agregar_linea_vertical
from lineas_flujo import agregar_red_de_flujo
from lineas_equipotenciales import extraer_pendientes, extraer_puntos, graficar_lineas_con_pendientes


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

    bezier_path_sup = agregar_red_de_flujo(ax, (0, 0), (52.5, 0), (105, 0), (157.5, 0), (210, 0), altura_base, False)
    bezier_path_ver = agregar_red_de_flujo(ax, (105, 0), (105, (C2-d)/2), (105, C2-d), (105, ((C2-d)*3)/2), (105, 2*(C2-d)), altura_base, False)
    pendientes_inicio, coordenadas_inicio = agregar_lineas_equipotenciales(ax, bezier_path_sup,8, longitud=10, color='red', grosor=0)
    pendientes_VER, coordenadas_VER = agregar_lineas_equipotenciales(ax, bezier_path_ver,8, longitud=10, color='red', grosor=0)
    
    distancia_1 = coordenadas_inicio['punto_1'][0]
    distancia_2 = coordenadas_inicio['punto_2'][0]
    distancia_3 = coordenadas_inicio['punto_3'][0]

    ver_1 = coordenadas_VER['punto_1'][1]
    ver_2 = coordenadas_VER['punto_2'][1]
    ver_3 = coordenadas_VER['punto_3'][1]
    '''
    bezier_path_1 = agregar_red_de_flujo(ax, (26.25, C1), (52.5,punto_1 ),(105, punto_1), (157.5, punto_1), (183.75, C2), altura_base)
    bezier_path_2 = agregar_red_de_flujo(ax, (26.25*2, C1), (65.625,punto_2 ), (105, punto_2), (144.375, punto_2),(183.75-26.25, C2), altura_base)
    bezier_path_3 = agregar_red_de_flujo(ax, (26.25*3, C1), (75.75,punto_3 ), (105, punto_3), (134.25, punto_3), (183.75-(26.25*2), C2), altura_base)
    '''

    bezier_path_1 = agregar_red_de_flujo(ax, (105-distancia_3, C1), (52.5,punto_1 ),(105, punto_1), (157.5, punto_1), (105+distancia_3, C2), altura_base, True)
    bezier_path_2 = agregar_red_de_flujo(ax, (105-distancia_2, C1), (65.625,punto_2 ), (105, punto_2), (144.375, punto_2),(105+distancia_2, C2), altura_base, True)
    bezier_path_3 = agregar_red_de_flujo(ax, (105-distancia_1, C1), (75.75,punto_3 ), (105, punto_3), (134.25, punto_3), (105+distancia_1, C2), altura_base, True)
    bezier_path_4 = agregar_red_de_flujo(ax, (0, 0), (52.5, 0), (105, 0), (157.5, 0), (210, 0), altura_base, True)

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
    #graficar_lineas_con_pendientes(ax, coordenadas, pendientes, color='green', grosor=1)

    # Guardar la figura usando el objeto ax
    plt.savefig(f"{nombre}.pdf", format='pdf', bbox_inches='tight', pad_inches=0)

# Ejemplo de uso
graficar(caso_1, 'caso_1', 50)
graficar(caso_2, 'caso_2', 50)
graficar(caso_3, 'caso_3', 50)