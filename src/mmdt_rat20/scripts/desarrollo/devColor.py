#!/usr/bin/env python2.7

import cv2
import numpy as np

# def show_image(img):
#     cv2.imshow("Image Window", img)
#     cv2.waitKey(3)

# matriz= np.array([[[10,20,30],[10,25,30],[30,54,25]],[[10,20,30],[10,25,30],[30,54,25]]])
# # cv2.namedWindow("Image Window", 1)
# # show_image(matriz)
# cv2.imshow("Image Window", matriz)


# img = np.zeros([5,5,3])

# img[:,:,0] = np.ones([5,5])*64/255.0
# img[:,:,1] = np.ones([5,5])*128/255.0
# img[:,:,2] = np.ones([5,5])*192/255.0

# cv2.imwrite('color_img.jpg', img)
# cv2.imshow("image", img)
# cv2.waitKey()


# ******************EN VECTOR, BUSQUEDA DE ELEMENTOS MAYOR QUE... ****************
# a = np.arange(1, 10)
# idx = np.where(a > 4)[0]    # Retorna los indices
# elts = a[a > 4]             # Retorna los elementos
# print(elts)

# ******************EN Matrix, BUSQUEDA DE ELEMENTOS MAYOR QUE... ****************
# mat= np.array([[0.25,0.26,0.25,0.26,0.7,0.7],[0.25,0.26,0.25,0.26,0.7,0.7],[0.8,0.8,0.8,1,1.3,1.3]])

# distMax= 1.3

# idxMatRBool = mat<0.5
# matR= idxMatRBool*1
# print(matR)

# idxMatGBool_a = mat>0.5
# idxMatGBool_b = mat<0.9
# matG_a= idxMatGBool_a*1
# matG_b= idxMatGBool_b*1
# matG= matG_a*matG_b
# print(matG)

# idxMatBBool = mat>0.9
# matB= idxMatBBool*1
# print(matB)

# img = np.zeros([3,6,3])
# img[:,:,0] = matR
# img[:,:,1] = matG
# img[:,:,2] = matB

# cv2.imshow("image", img)
# cv2.waitKey()



# ****************** ARMADO DE MATRIX POR COLOR ****************
mat= np.array([[0.1,0.26,0.25,0.26,0.7,0.7],[0.15,0.26,0.25,0.26,0.7,0.7],[0.8,0.8,0.8,1,1.3,1.3]])

tamW= 6
tamH= 3

distMax= 1.3
dist2= distMax/2

idxMatRBool = mat<dist2
matR= idxMatRBool*1

idxMatBBool = mat>dist2
matB= idxMatBBool*1

matG = np.zeros([tamH,tamW])
for kW in range(0,tamW-1):
    for kH in range(0,tamH-1):
        distancia= mat[kH,kW]
        if distancia>dist2:
            m= -1/(distMax-dist2)
            b= distMax/(m*distancia)
            colorG= m*distancia + b
        else:
            m= 1/dist2
            b= 0
            colorG= m*distancia + b
        matG[kH][kW]= colorG

img = np.zeros([tamH,tamW,3])
img[:,:,0] = matB
img[:,:,1] = matG
img[:,:,2] = matR

imgA= np.uint8(img*255)
print(matB*0.15)
# print(imgA)

# cv2.imshow("image", img)
# cv2.waitKey()