def extraer_puntos(lista_diccionarios, i):
    lista_coordenadas = []

    for diccionario in lista_diccionarios:
        # Verificar si el diccionario contiene 'punto_1'
        if f'punto_{i}' in diccionario:
            if isinstance(diccionario[f'punto_{i}'], tuple):
                # Si es una tupla, son coordenadas
                lista_coordenadas.append(diccionario[f'punto_{i}'])
            
    return lista_coordenadas

def extraer_pendientes(lista_diccionarios, i):
    lista_pendientes = []

    for diccionario in lista_diccionarios:
        # Verificar si el diccionario contiene 'punto_1'
        if f'punto_{i}' in diccionario:
            if isinstance(diccionario[f'punto_{i}'], float):
                # Si es un flotante, es una pendiente
                lista_pendientes.append(diccionario[f'punto_{i}'])
            
    return lista_pendientes


def graficar_lineas_con_pendientes(ax, coor, m, color='blue', grosor=1):

    # for i in range(len(coordenadas[0])):

    #     if i == 0:
    #         continue

    #     # Extraer las coordenadas y pendientes de cada punto
    #     coor = extraer_puntos(coordenadas , i)
    #     m = extraer_pendientes(pendientes, i)

    #     if i == 1:
    #         break

    #     i += 1

    # Extraer las coordenadas X e Y de las coordenadas
    x_coords = [c[0] for c in coor]
    y_coords = [c[1] for c in coor]

    print(x_coords)
    print(y_coords)
    print(m)

    # #Checkeo que x sea en orden ascendente
    # if x_coords != sorted(x_coords):
    #     x_coords = x_coords [::-1]  # Invertir la lista si no está en orden ascendente
    #     y_coords = y_coords [::-1]
    #     m = m [::-1]

    print(x_coords)
    print(m)

    # Crear el spline cúbico hermítico que respeta las pendientes (derivadas)
    spline = CubicHermiteSpline(x_coords, y_coords, m)

    # Generar puntos adicionales para graficar la curva suavemente
    x_new = np.linspace(min(x_coords), max(x_coords), 100)
    y_new = spline(x_new)

    # Dibujar la curva en el gráfico
    ax.plot(x_new, y_new, color=color, linewidth=grosor)