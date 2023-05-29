#!/usr/bin/env python2.7

import cv2
import math
import numpy as np

a= np.array([[float('nan'),0.26,0.25,0.26,0.7,float('nan')],[0.15,0.26,0.25,0.26,0.7,0.7],[0.8,0.8,0.8,1,1.3,1.3]])
print(a)

print(np.argwhere(np.isnan(a)))

sinNan= np.isnan(a)
a[sinNan]=10
print(a)

print(a*10+2)