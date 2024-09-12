from variables import caso_1, caso_2, caso_3, num_equipotenciales, k, gamma_agua, gamma_sturada
from grafico import graficar, graficar_lineas_con_pendientes
from matplotlib import pyplot as plt


def presiones_poros(caso, nombre):

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
    

    ax, pendientes, coordenadas = graficar(caso, 'nombre', 50)

    #las coordenadas de la ataguia son
    coordenadas_ata = coordenadas[-1]
    print(coordenadas_ata)





    # Llamar a la función para graficar las líneas
    graficar_lineas_con_pendientes(ax, coordenadas, pendientes, color='green', grosor=1)

    # Guardar la figura usando el objeto ax
    plt.savefig(f"{nombre}.pdf", format='pdf', bbox_inches='tight', pad_inches=0)


presiones_poros(caso_1, 'caso_1')
presiones_poros(caso_2, 'caso_2')
presiones_poros(caso_3, 'caso_3')
    

    