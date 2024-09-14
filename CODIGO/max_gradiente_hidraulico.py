#Aqui calculare el maximo graidente hidraulico

from variables import caso_1, caso_2, caso_3, num_equipotenciales

def max_gradiente_hidraulico(caso):

    C1 = caso['c1']
    C2 = caso['c2']
    D = caso['d']
    B1 = caso['b1']
    B2 = caso['b2']

    Delta_H = (C1+B1) - (C2+B2)

    print(f'{C1=}, {C2=}, {D=}')

    max_g = Delta_H/((C1-C2) + 2*D)

    print(f'{max_g=}')
    print('')

max_gradiente_hidraulico(caso_1)
max_gradiente_hidraulico(caso_2)
max_gradiente_hidraulico(caso_3)