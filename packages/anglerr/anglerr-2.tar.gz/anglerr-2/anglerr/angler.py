from scipyy import scipyy
import numpy as np

print(scipyy.number4.__doc__)

n1, p1 = 180, 0.93
n2, p2 = 70, 0.92
var_S1 = n1 * p1 * (1 - p1)
var_S2 = n2 * p2 * (1 - p2)
var_S = var_S1 + var_S2
std_S = np.sqrt(var_S)
skew_S1 = (1 - 2 * p1) / np.sqrt(n1 * p1 * (1 - p1))
skew_S2 = (1 - 2 * p2) / np.sqrt(n2 * p2 * (1 - p2))
combined_skewness = (skew_S1 * var_S1**1.5 + skew_S2 * var_S2**1.5) / var_S**1.5
print()