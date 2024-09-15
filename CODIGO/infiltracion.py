from variables import caso_1, caso_2, caso_3, num_equipotenciales, k

def infiltracion (caso):
    C1 = caso['c1']
    C2 = caso['c2']
    B1 = caso['b1']
    B2 = caso['b2']
    d = caso['d']

    hl = (C1+B1) - (C2+B2)
    inf = k*hl*(3/(num_equipotenciales))*24*3600 #m3/dia

    return inf
    

print('caso 1',infiltracion(caso_1))
print('caso 2',infiltracion(caso_2))
print('caso 3',infiltracion(caso_3))