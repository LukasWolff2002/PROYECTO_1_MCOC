from variables import caso_1, caso_2, caso_3, num_equipotenciales, k, gamma_agua, gamma_sturada
from grafico import graficar, graficar_lineas_con_pendientes
from matplotlib import pyplot as plt
from scipy.interpolate import griddata
from matplotlib.path import Path
import numpy as np

def crear_mascara_en_forma_L(grid_x, grid_y, coordenadas_l):
    """Crea una máscara en forma de 'L' usando las coordenadas definidas."""
    # Crear el camino o Path de la forma 'L' con las coordenadas dadas
    poligono_l = Path(coordenadas_l)

    # Crear una máscara que es True dentro de la forma 'L' y False fuera
    puntos = np.vstack((grid_x.ravel(), grid_y.ravel())).T
    mascara = poligono_l.contains_points(puntos).reshape(grid_x.shape)
    
    return mascara

def agregar_mapa_calor_con_mascara_L(ax, diccionario_presion, coordenadas_l, cmap='YlOrRd'):
    # Extraer las coordenadas (x, y) y las presiones
    x_coords = np.array([key[0] for key in diccionario_presion.keys()])
    y_coords = np.array([key[1] for key in diccionario_presion.keys()])
    presiones = np.array(list(diccionario_presion.values()))

    # Crear una cuadrícula regular para interpolar las presiones
    grid_x, grid_y = np.mgrid[min(x_coords):max(x_coords):100j, min(y_coords):max(y_coords):100j]

    # Interpolación de los datos de presión en la cuadrícula
    grid_presion = griddata((x_coords, y_coords), presiones, (grid_x, grid_y), method='cubic')

    # Crear la máscara en forma de 'L'
    mascara_l = crear_mascara_en_forma_L(grid_x, grid_y, coordenadas_l)

    # Aplicar la máscara a la matriz de presiones
    grid_presion[~mascara_l] = np.nan  # Poner NaN fuera de la forma 'L'

    # Obtener los valores mínimos y máximos de presión para ajustar la escala
    vmin = np.nanmin(grid_presion)
    vmax = np.nanmax(grid_presion)

    # Agregar el mapa de calor al gráfico ajustando los valores min/max para mayor contraste
    heatmap = ax.imshow(grid_presion.T, extent=(min(x_coords), max(x_coords), min(y_coords), max(y_coords)), 
                        origin='lower', cmap=cmap, alpha=0.6, vmin=vmin, vmax=vmax)

    # Dibujar el contorno de la forma 'L'
    poligono_l = plt.Polygon(coordenadas_l, fill=None, edgecolor='black', linewidth=2)
    ax.add_patch(poligono_l)

    # Agregar barra de color dentro de la figura
    cbar = plt.colorbar(heatmap, ax=ax, orientation='vertical', fraction=0.05, pad=0.04)
    
    # Ajustar la escala de la leyenda de presión
    cbar.set_label('Presión KPa', fontsize=16)  # Etiqueta de la barra de colores
    cbar.ax.tick_params(labelsize=12)  # Tamaño del texto de la leyenda
    cbar.set_ticks([vmin, (vmin + vmax) / 2, vmax])  # Ajustar los ticks de la barra de colores
    cbar.ax.set_position([0.75, 0.1, 0.02, 1.2])  # [left, bottom, width, height] dentro del gráfico



def presiones_poros(caso, nombre, altura_rel):

    presiones = {}

    C1 = caso['c1']
    C2 = caso['c2']
    B1 = caso['b1']
    B2 = caso['b2']
    A1 = caso['a1']
    A2 = caso['a2']
    
    presiones['A'] = 0
    presiones['H'] = 0
    presiones['B'] = B1*gamma_agua
    presiones['G'] = B1*gamma_agua

    #Calculo delta h
    Delta_H = (C1+B1) - (C2+B2)
    Nd = num_equipotenciales - 1
    delta_h = Delta_H/Nd
    

    ax, pendientes, coordenadas = graficar(caso, 'nombre', altura_rel)

    #las coordenadas de la ataguia son
    coordenadas_ata = coordenadas[-1]
    print('')
    print(coordenadas_ata)



    #Mapa de calor
    mapa_calor = {}

    #Primero nesecito la altura relativa = suelo
    for diccionarios in coordenadas:

        
        for elemento in diccionarios:
            z = ((diccionarios[elemento][1]-altura_rel)*200)/1000
            Zg = z
            ni = int(elemento.split('_')[1])
            Delta_Hi = (C1+B1)-((Delta_H*ni)/Nd)
            hp = Delta_Hi-Zg
            u = (hp*gamma_agua)/1000
            mapa_calor[diccionarios[elemento]]= u

    print(mapa_calor)

    coordenadas_l = [(0, (C1*1000)/200 + altura_rel), (105, (C1*1000)/200+altura_rel), (105, ((C2)*1000)/200+altura_rel), (210, ((C2)*1000)/200+altura_rel), (210, 0 +altura_rel), (0, 0+altura_rel)]
    
    agregar_mapa_calor_con_mascara_L(ax, mapa_calor, coordenadas_l)








    # Llamar a la función para graficar las líneas
    graficar_lineas_con_pendientes(ax, coordenadas, pendientes, color='green', grosor=1)

    # Guardar la figura usando el objeto ax
    plt.savefig(f"{nombre}.pdf", format='pdf', bbox_inches='tight', pad_inches=0)
    print('')

presiones_poros(caso_1, 'caso_1', 50)
presiones_poros(caso_2, 'caso_2', 50)
presiones_poros(caso_3, 'caso_3', 50)
    

    