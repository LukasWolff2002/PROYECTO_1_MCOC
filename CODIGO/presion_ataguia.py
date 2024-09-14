#Ok, ahora se que para calcular la presion en la ataguia, nesecito el ultimo diccionario, donde

from variables import caso_1, caso_2, caso_3, num_equipotenciales, k, gamma_agua, gamma_sturada
from grafico import graficar, graficar_lineas_con_pendientes
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
from scipy.interpolate import interp1d
from math import ceil as ceil

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

def presiones_ataguia(caso, nombre, altura_rel):

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

    if nombre != 'caso_1':
        for clave in claves[mitad:]:
            #ahora calculo la presion de poros
            z = ((coor[clave][1]-altura_rel)*200)/1000
            Zg = z
            ni = int(clave.split('_')[1])
            Delta_Hi = (C1+B1)-((Delta_H*ni)/Nd)
            hp = Delta_Hi-Zg
            u = (hp*gamma_agua)/1000
            derecha[coor[clave][1]] = u



    
    #neto = restar_diccionarios(izquierda, derecha)
    #graficar_diccionario(ax, neto, False, color='red') 

    print(f'{izquierda=}')
    print(f'{derecha=}') 
    
    for claves in derecha.keys():
        derecha[claves] += 105

    for claves in izquierda.keys():
        izquierda[claves] = 105 - izquierda[claves]

    derecha[Altura_agua_der] = 105

    if nombre == 'caso_1':
        derecha[(((C2)*1000)/200)+altura_rel+0.1] = 105+(((B2)*1000)/200)*gamma_agua

    graficar_diccionario(ax, izquierda, False, color='blue')
    graficar_diccionario(ax, derecha, True, color='blue')

    
    x_known = list(izquierda.keys())
    y_known = list(izquierda.values())

    # Crear la función de interpolación
    interpolacion = interp1d(x_known, y_known, kind='linear')

    incognitas = list(derecha.keys())

    interpolado = {}

    # Calcular los valores de y para las incógnitas
    for values in incognitas:
        values_aprox = ceil(values)
        print(f'{values=}, {encontrar_y(interpolacion, values_aprox)}')
        interpolado[values] = float(encontrar_y(interpolacion, values_aprox))

    
    print(f'{interpolado=}')
    max_interpolado = max(interpolado.keys())

    print(f'{max_interpolado=}')
    
    neto = []
    #Oke, primero me tengo que quedar con todas las claves de izquierda que sean mayores a las claves de interpolado
    for claves in izquierda.keys():
        if claves > max_interpolado:
            neto.append([claves,izquierda[claves]])

    #Luego agrego el maximo
    neto.append([max_interpolado, interpolado[max_interpolado]])

    print(f'{neto=}')

    #Ahora comienzo con la resata
    for claves in derecha.keys():
        print(f'{claves=}')
        if claves == 129.5:
            print(-derecha[claves] + interpolado[claves])
        neto.append([claves,derecha[claves] - interpolado[claves]])

    print(f'{neto=}')

    # Ordenar las sublistas por el primer elemento en orden descendente
    neto_ordenada = sorted(neto, key=lambda x: x[0], reverse=True)

    print(f'{neto_ordenada=}')

    graficar_lista(ax, neto_ordenada, color='red')
            



    # Llamar a la función para graficar las líneas
    graficar_lineas_con_pendientes(ax, coordenadas, pendientes, color='green', grosor=1)

    # Guardar la figura usando el objeto ax
    plt.savefig(f"{nombre}.pdf", format='pdf', bbox_inches='tight', pad_inches=0)




    #luego al lado derecho

presiones_ataguia(caso_1, 'caso_1', 50)
# presiones_ataguia(caso_2, 'caso_2', 50)
# presiones_ataguia(caso_3, 'caso_3', 50)
    