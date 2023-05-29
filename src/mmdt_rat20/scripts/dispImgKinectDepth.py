#!/usr/bin/env python
# Import ROS libraries and messages
import rospy
import numpy as np
import math
from sensor_msgs.msg import Image

from matplotlib import pyplot as plt
from matplotlib import image as mpimg


# Import OpenCV libraries and tools
import cv2
from cv_bridge import CvBridge, CvBridgeError


  # Print "Hello!" to terminal
# print "Hello!"

# Initialize the ROS Node named 'opencv_example', allow multiple nodes to be run with this name
# rospy.init_node('opencv_example', anonymous=True)
rospy.init_node('opencv_example', anonymous=False)

# Print "Hello ROS!" to the Terminal and to a ROS Log file located in ~/.ros/log/loghash/*.log
rospy.loginfo("Hello ROS!")

# Initialize the CvBridge class
bridge = CvBridge()

# Define a function to show the image in an OpenCV Window
def show_image(img):
    cv2.imshow("Imagen Profundidad", img)
    cv2.waitKey(3)

    # plt.imshow(img)
    # plt.pause(0.01)
    # plt.show()
    # cv2.destroyAllWindows()

# Define a callback for the Image message
def image_callback(img_msg):
    # print('Recibi imagen')
    # rate = rospy.Rate(100)
    # log some info about the image topic
    # rospy.loginfo(img_msg.header)

    # Try to convert the ROS Image message to a CV2 Image
    try:
        tamW= 800
        tamH= 400
        distMax= 2.0
        dist2= distMax*0.3

        cv_image = np.zeros([tamH,tamW])
        cv_image = bridge.imgmsg_to_cv2(img_msg, "passthrough")

        mat = np.zeros([tamH,tamW])
        mat= cv_image

        # print(np.argwhere(np.isnan(mat)))

        sinNan= np.isnan(mat)
        mat.setflags(write=1)
        mat[sinNan]=5.0

        idxMatRBool = mat<dist2
        matR= idxMatRBool*1

        idxMatBBool = mat>dist2
        matB= idxMatBBool*1

        # matG = np.zeros([tamH,tamW])
        m1= -1/(distMax-dist2)
        b1= distMax*matB
        matG_a= m1*matB*mat + b1

        m2= 1/dist2
        matG_b= m2*matR*mat

        matG= matG_a + matG_b
        # print(matG_a[1:10,1:10])
        # matG= np.ones([tamH,tamW])

        img = np.zeros([tamH,tamW,3])
        img[:,:,0] = matB           # Corresponde al color azul
        img[:,:,1] = matG           # Corresponde al color verde
        img[:,:,2] = matR           # Corresponde al color rojo
        # imgA= np.uint8(img*255)

        # img[:,:,0] = 0*np.ones([tamH,tamW])         # Corresponde al color azul
        # img[:,:,1] = 0*np.ones([tamH,tamW])         # Corresponde al color verde
        # img[:,:,2] = 1*np.ones([tamH,tamW])        # Corresponde al color rojo
        # imgA= img

    except CvBridgeError, e:
        rospy.logerr("CvBridge Error: {0}".format(e))

    # print(img[280:300,1,:])         # Ultimas filas de la primera columna
    # print(img[1:2,1,:])
    show_image(img)

    # show_image(cv_image)
    # rate.sleep()
# Initalize a subscriber to the "/camera/rgb/image_raw" topic with the function "image_callback" as a callback
sub_image = rospy.Subscriber("/3D_camera/depth/image_raw", Image, image_callback, queue_size=1,                                
                             buff_size=2 ** 31 - 1)
# sub_image = rospy.Subscriber("/3D_camera/color/image_raw", Image, image_callback)

# Initialize an OpenCV Window named "Image Window"
# cv2.namedWindow("Imagen Profundidad", 1)

# Loop to keep the program from shutting down unless ROS is shut down, or CTRL+C is pressed
while not rospy.is_shutdown():
    rospy.spin()