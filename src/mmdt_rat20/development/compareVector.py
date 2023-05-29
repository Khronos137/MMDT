#!/usr/bin/env python
import numpy as np

# vector1 = np.array([1.0,0.0,0.0])
# vector2 = np.array([1.0,1.0,0.0])
vector1 = [2.0,0.0,0.0]
vector2 = [1.0,1.0,0.0]

print(np.array_equal(vector1,vector2))
if np.array_equal(vector1,vector2)==0:
    print('Vectores no iguales!')
else:
    print('Vectores iguales!')

print('SEGUNDA PRUEBA:****')
# vecComp= np.array_equal(vector1,vector2)
vecComp= np.array(vector1)==np.array(vector2)
print(vecComp)
print(vecComp[2])