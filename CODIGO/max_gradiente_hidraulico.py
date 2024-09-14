#Aqui calculare el maximo graidente hidraulico

from variables import caso_1, caso_2, caso_3, gamma_agua, gamma_sturada

def max_gradiente_hidraulico(caso, nombre):

    C1 = caso['c1']
    C2 = caso['c2']
    D = caso['d']
    B1 = caso['b1']
    B2 = caso['b2']

    Delta_H = (C1+B1) - (C2+B2)

    max_g = Delta_H/((C1-C2) + 2*D)

    ic = (gamma_sturada-gamma_agua)/gamma_agua

    FS = ic/max_g

    print(f'{nombre} {max_g=} {ic=} {FS=}')
    if ic <= max_g:
        print('Hay licuefaccion')

    else:
        print('No hay licuefaccion')
    print('')

max_gradiente_hidraulico(caso_1, 'caso_1')
max_gradiente_hidraulico(caso_2, 'caso_2')
max_gradiente_hidraulico(caso_3, 'caso_3')