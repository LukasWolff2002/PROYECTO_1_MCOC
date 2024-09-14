import numpy as np
from scipy.integrate import simps

dict = {112.00000000000001: 105, 93.0: 67.722, 72.60208142026323: 40.594426603699276, 58.923477196204466: 26.650147973238873, 51.839914294459746: 25.645340417158565}

x = np.array(list(dict.keys()))
y = np.array(list(dict.values()))

# Calcular el área bajo la curva usando integración numérica (Simpson)
area = simps(y, x)

# Centroide en x: x_bar = (1/Area) * ∫ x * y dx
x_bar = simps(x * y, x) / area

# Centroide en y: y_bar = (1/Area) * ∫ (1/2) * y^2 dx
y_bar = simps(0.5 * y**2, x) / area

print(f"Centroide: x_bar = {x_bar}, y_bar = {y_bar}")