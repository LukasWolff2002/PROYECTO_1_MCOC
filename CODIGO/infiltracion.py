from variables import caso_1, caso_2, caso_3, num_equipotenciales, d, k

def infiltracion (caso):
    C1 = caso['c1']
    C2 = caso['c2']
    B1 = caso['b1']
    B2 = caso['b2']

    hl = (C1+B1) - (C2+B2)
    
    inf = k*hl*(d/(hl+B2+d))*24*3600 #m3/dia

    return inf
    

infiltracion(caso_1)