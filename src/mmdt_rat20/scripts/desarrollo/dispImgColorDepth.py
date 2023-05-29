#!/usr/bin/env python
# Import ROS libraries and messages
import rospy
import numpy as np
import math
from sensor_msgs.msg import Image

# Import OpenCV libraries and tools
import cv2
from cv_bridge import CvBridge, CvBridgeError
global img_depth
global img_color
global tamW_depth
global tamH_depth
global distMax
global dist2

tamW_depth= 200
tamH_depth= 150
distMax= 2.0
dist2= distMax*0.3

tamW_color= 700
tamH_color= 300
img_depth = np.zeros([tamH_depth,tamW_depth,3])
img_color = np.zeros([tamH_color,tamW_color,3])


# Define a function to show the image in an OpenCV Window
def show_image(img):
    cv2.imshow("Imagen Profundidad", img)
    cv2.waitKey(3)

# def image_callback(img_msg):
#     # log some info about the image topic
#     # rospy.loginfo(img_msg.header)
#     global img_color
#     # Try to convert the ROS Image message to a CV2 Image
#     try:
#         # img_colorRaw = bridge.imgmsg_to_cv2(img_msg, "passthrough")
#         img_color = bridge.imgmsg_to_cv2(img_msg, "passthrough")

#         # colorR= img_colorRaw[:,:,0]
#         # colorG= img_colorRaw[:,:,1]
#         # colorB= img_colorRaw[:,:,2]

#         # img_color[:,:,0]= colorB/255.0
#         # img_color[:,:,1]= colorG/255.0
#         # img_color[:,:,2]= colorR/255.0

#     except CvBridgeError, e:
#         rospy.logerr("CvBridge Error: {0}".format(e))

# Define a callback for the Image message
def image_callback(img_msg):
    # print('Recibi imagen')
    global img_depth
    global tamW_depth
    global tamH_depth
    global distMax
    global dist2
    

    # Try to convert the ROS Image message to a CV2 Image
    try:
        # cv_image = np.zeros([tamH_depth,tamW_depth])
        img_colorRaw = bridge.imgmsg_to_cv2(img_msg, "passthrough")
        # print(len(img_colorRaw.shape))
        
        if len(img_colorRaw.shape)==3:
            img_depth=img_colorRaw
        # mat = np.zeros([tamH_depth,tamW_depth])
        # mat= cv_image

        # # sinNan= np.isnan(mat)
        # # mat.setflags(write=1)
        # # mat[sinNan]=5.0

        # idxMatRBool = mat<dist2
        # matR= idxMatRBool*1

        # idxMatBBool = mat>dist2
        # matB= idxMatBBool*1

        # # matG = np.zeros([tamH_depth,tamW_depth])
        # m1= -1/(distMax-dist2)
        # b1= distMax*matB
        # matG_a= m1*matB*mat + b1

        # m2= 1/dist2
        # matG_b= m2*matR*mat

        # matG= matG_a + matG_b

        # img_depth = np.zeros([tamH_depth,tamW_depth,3])
        # img_depth[:,:,0] = matB           # Corresponde al color azul
        # img_depth[:,:,1] = matG           # Corresponde al color verde
        # img_depth[:,:,2] = matR           # Corresponde al color rojo

    except CvBridgeError, e:
        rospy.logerr("CvBridge Error: {0}".format(e))

    # show_image(img_depth)

def ejecutable():
    k=0
    rate = rospy.Rate(50)
    # global img_depth
    # depth_image = rospy.Subscriber("/3D_camera/depth/image_raw", Image, image_callback_depth)
    # Loop to keep the program from shutting down unless ROS is shut down, or CTRL+C is pressed
    while not rospy.is_shutdown():
        show_image(img_depth)
        k=k+1
        # print(k)
        # img_color.setflags(write=1)
        # img_mixta= img_color
        # img_mixta[0:tamH_depth,tamW_color-tamW_depth:tamW_color,:]= img_depth
        # show_image(img_color)
        
        # rate.sleep()
        # show_image(img_mixta)
        # rospy.spin()

# # Initialize the CvBridge class
# bridge = CvBridge()

# rospy.init_node('opencv_example', anonymous=True)

# # Print "Hello ROS!" to the Terminal and to a ROS Log file located in ~/.ros/log/loghash/*.log
# rospy.loginfo("Hello ROS!")

# # Initalize a subscriber to the "/camera/rgb/image_raw" topic with the function "image_callback" as a callback
# depth_image = rospy.Subscriber("/3D_camera/depth/image_raw", Image, image_callback_depth)
# color_image = rospy.Subscriber("/mmdt_rat20/cameraTop/image_raw", Image, image_callback_color)

if __name__ == '__main__':
    try:

        # Initialize the CvBridge class
        bridge = CvBridge()

        rospy.init_node('opencv_example', anonymous=True)

        # Print "Hello ROS!" to the Terminal and to a ROS Log file located in ~/.ros/log/loghash/*.log
        rospy.loginfo("Hello ROS!")

        # Initalize a subscriber to the "/camera/rgb/image_raw" topic with the function "image_callback" as a callback
        # depth_image = rospy.Subscriber("/3D_camera/depth/image_raw", Image, image_callback, queue_size=1,                                
        #                      buff_size=2 ** 31 - 1)
        color_image = rospy.Subscriber("/mmdt_rat20/cameraTop/image_raw", Image, image_callback, queue_size=1,                                
                             buff_size=2 ** 31 - 1)

        ejecutable()
    except rospy.ROSInterruptException:
        pass