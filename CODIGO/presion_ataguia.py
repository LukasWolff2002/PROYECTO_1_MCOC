#Ok, ahora se que para calcular la presion en la ataguia, nesecito el ultimo diccionario, donde

from variables import caso_1, caso_2, caso_3, num_equipotenciales, k, gamma_agua, gamma_sturada, altura_rel
from grafico import graficar, graficar_lineas_con_pendientes
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
from scipy.interpolate import interp1d
from math import ceil as ceil
from scipy.integrate import simps
from lineas import agregar_linea_horizontal

    # Función para encontrar el valor de y para un valor de x
def encontrar_y(interpolacion, x):
    return interpolacion(x)

def graficar_diccionario (ax, diccionario, reflexion, color):

    # Extraer las claves y los valores del diccionario
    y_values = list(diccionario.keys())
    x_values = list(diccionario.values())

    # Dibujar los puntos en la gráfica
    ax.scatter(x_values, y_values, color=color, label='Puntos')

    # Unir los puntos con líneas
    ax.plot(x_values, y_values, color=color, linestyle='-', label='Líneas')

# Definir la función para graficar
def graficar_lista(ax, lista, color):
    # Separar las claves (primer elemento) y los valores (segundo elemento)
    y_values = [sublista[0] for sublista in lista]
    x_values = [sublista[1] for sublista in lista]

    # Dibujar los puntos en la gráfica
    ax.scatter(x_values, y_values, color=color, label='Puntos')

    # Unir los puntos con líneas
    ax.plot(x_values, y_values, color=color, linestyle='-', label='Líneas')
    
    


def mantener_ultima_si_iguales(diccionario):
    # Obtener todas las claves del diccionario
    claves = list(diccionario.keys())
    
    # Verificar si todas las claves son iguales
    if all(clave == claves[0] for clave in claves):
        # Si todas las claves son iguales, devolver solo la última clave y su valor
        ultima_clave = claves[-1]
        diccionario = {ultima_clave: diccionario[ultima_clave]}
    
    return diccionario

'''
def restar_diccionarios(izquierda, derecha, x_reflexion=105):
    # Obtener las claves y valores de izquierda y derecha
    y_izquierda = np.array(list(izquierda.keys()))
    x_izquierda = np.array(list(izquierda.values()))
    
    y_derecha = np.array(list(derecha.keys()))
    x_derecha = np.array(list(derecha.values())) 

    # Reflejar la curva derecha respecto a x_reflexion
    x_derecha_reflejado = 2 * x_reflexion - x_derecha

    # Interpolar los valores reflejados de la curva derecha a los valores de y de la curva izquierda
    interp_derecha_reflejada = interp1d(y_derecha, x_derecha_reflejado, fill_value="extrapolate")
    x_derecha_interpolado = interp_derecha_reflejada(y_izquierda)

    # Restar los valores de las dos curvas (considerando que en un punto la resta será 0)
    resultado_x = x_izquierda + x_derecha

    # Crear el diccionario de resultado
    resultado = dict(zip(y_izquierda, resultado_x))

    print('resultado',resultado)

    return resultado 
'''

def presiones_ataguia(caso, nombre, altura_rel, extension):

    C1 = caso['c1']
    C2 = caso['c2']
    B1 = caso['b1']
    B2 = caso['b2']
    A1 = caso['a1']
    A2 = caso['a2']

    Delta_H = (C1+B1) - (C2+B2)
    Nd = num_equipotenciales - 1

    Altura_agua_iz = ((C1+B1)*1000)/200 + altura_rel
    Altura_agua_der = ((C2+B2)*1000)/200 + altura_rel

    izquierda = {Altura_agua_iz: 0}
    derecha = {}

    ax, pendientes, coordenadas = graficar(caso, 'nombre', altura_rel)

    # Convertir las claves del diccionario en una lista
    coor = coordenadas[-1]
    claves = list(coor.keys())

    # Calcular el punto medio
    mitad = len(claves) // 2

    # Iterar sobre la primera mitad
    for clave in claves[:mitad]:
        #ahora calculo la presion de poros
        z = ((coor[clave][1]-altura_rel)*200)/1000
        Zg = z
        ni = int(clave.split('_')[1])
        Delta_Hi = (C1+B1)-((Delta_H*ni)/Nd)
        hp = Delta_Hi-Zg
        u = (hp*gamma_agua)/1000
        izquierda[coor[clave][1]] = u

        # Iterar sobre la segunda mitad

    for clave in claves[mitad:]:
        #ahora calculo la presion de poros
        z = ((coor[clave][1]-altura_rel)*200)/1000
        Zg = z
        ni = int(clave.split('_')[1])
        Delta_Hi = (C1+B1)-((Delta_H*ni)/Nd)
        hp = Delta_Hi-Zg
        u = (hp*gamma_agua)/1000
        if nombre == 'caso_1':
            derecha[coor[clave][1]+0.01] = u
            break
        derecha[coor[clave][1]] = u

    
    #neto = restar_diccionarios(izquierda, derecha)
    #graficar_diccionario(ax, neto, False, color='red') 
    
    for claves in derecha.keys():
        derecha[claves] += 105

    for claves in izquierda.keys():
        izquierda[claves] = 105 - izquierda[claves]

    derecha[Altura_agua_der] = 105

    x_known = list(izquierda.keys())
    y_known = list(izquierda.values())

    # Crear la función de interpolación
    interpolacion = interp1d(x_known, y_known, kind='linear')

    incognitas = list(derecha.keys())

    interpolado = {}

    # Calcular los valores de y para las incógnitas
    for values in incognitas:
        values_aprox = ceil(values)
        interpolado[values] = float(encontrar_y(interpolacion, values_aprox))

    
    max_interpolado = max(interpolado.keys())
    
    neto = []
    #Oke, primero me tengo que quedar con todas las claves de izquierda que sean mayores a las claves de interpolado
    for claves in izquierda.keys():
        if claves > max_interpolado:
            neto.append([claves,izquierda[claves]])

    #Luego agrego el maximo
    neto.append([max_interpolado, interpolado[max_interpolado]])


    #Ahora comienzo con la resata
    for claves in derecha.keys():
        neto.append([claves,derecha[claves]-105 + interpolado[claves]])



    # Ordenar las sublistas por el primer elemento en orden descendente
    neto_ordenada = sorted(neto, key=lambda x: x[0], reverse=True)


    #graficar_diccionario(ax, izquierda, False, color='blue')
    #graficar_diccionario(ax, derecha, True, color='blue')
    graficar_lista(ax, neto_ordenada, color='red')

    x = np.array([sublista[0] for sublista in neto_ordenada])
    y = np.array([sublista[1] for sublista in neto_ordenada])

    # Calcular el área bajo la curva usando la regla de Simpson
    area = simps(y, x)

    # Centroide en x: x_bar = (1/Area) * ∫ x * y dx
    x_bar = simps(x * y, x) / area

    # Centroide en y: y_bar = (1/Area) * ∫ (1/2) * y^2 dx
    y_bar = simps(0.5 * y**2, x) / area

    print(f"Centroide: x_bar = {x_bar}, y_bar = {y_bar}")

    #Ahora grafico el centroide

    agregar_linea_horizontal(ax, x_bar + altura_rel, 0, 210, 'red') #Linea de A1
    
    # Quiero obtener las presiones en ciertos puntos

    x_known = list(izquierda.keys())
    y_known = list(izquierda.values())

    interpolacion = interp1d(x_known, y_known, kind='linear')

    A = ((B1+C1)*1000)/200 +altura_rel-1
    A = 105 - encontrar_y(interpolacion,ceil(A) )
    print(f'Presion en A: {A}')

    B = ((C1)*1000)/200 +altura_rel
    B = 105 - encontrar_y(interpolacion, ceil(B) )
    print(f'Presion en B: {B}')

    C = ((C2+B2)*1000)/200 +altura_rel
    C = 105 - encontrar_y(interpolacion, ceil(C) )
    print(f'Presion en C: {C}')

    D = ((C2)*1000)/200 +altura_rel+1
    D = 105 - encontrar_y(interpolacion, ceil(D) )
    print(f'Presion en D: {D}')

    E = 105 - min(y_known)
    print(f'Presion en E: {E}')

    x_known = list(derecha.keys())
    y_known = list(derecha.values())

    interpolacion = interp1d(x_known, y_known, kind='linear')

    F = max(y_known) - 105
    print(f'Presion en F: {F}')

    G = ((C2)*1000)/200 +altura_rel+1
    G = encontrar_y(interpolacion, ceil(G) ) - 105
    print(f'Presion en G: {G}')

    H = ((C2+B2)*1000)/200 +altura_rel
    H = encontrar_y(interpolacion, ceil(H) ) - 105
    print(f'Presion en H: {H}')







    


    # Llamar a la función para graficar las líneas
    graficar_lineas_con_pendientes(ax, coordenadas, pendientes, color='green', grosor=1)

    # Guardar la figura usando el objeto ax
    plt.savefig(f"{nombre+extension}.jpg", format='jpg', bbox_inches='tight', pad_inches=0)






    #luego al lado derecho

presiones_ataguia(caso_1, 'caso_1', altura_rel, '_centroide_y')
presiones_ataguia(caso_2, 'caso_2', altura_rel, '_centroide_y')
presiones_ataguia(caso_3, 'caso_3', altura_rel, '_centroide_y')
    