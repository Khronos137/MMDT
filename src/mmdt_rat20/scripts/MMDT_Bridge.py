#!/usr/bin/env python
import rospy
import math
import numpy as np
from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState
from gazebo_msgs.msg import LinkStates

global frameCommands
global robotPos
global robotVel
global gazebo_link_states
global referenceFrame
global chasisPos
global chasisVel
global a                # Distancia desde el CDG hacia el punto de interes

# robotPos = [platfPosX, platfPosY, orient, torsPosZ, torsPosY, manDerQ1..Q6, manIzqQ1..Q6]
# robotVel = [platfVelX, platfVelY, w, torsVelZ, torsVelY, manDerQ1_p..Q6_p, manIzqQ1_p..Q6_p]

frameCommands = [0.0,0.0,0.0,0.0, 0.0,0.0, 0.0,0.0,0.0,0.0,0.0,0.0, 0.0,0.0,0.0,0.0,0.0,0.0]
robotPos = [0.0,0.0,0.0, 0.0,0.0, 0.0,0.0,0.0,0.0,0.0,0.0, 0.0,0.0,0.0,0.0,0.0,0.0]  
robotVel = [0.0,0.0,0.0, 0.0,0.0, 0.0,0.0,0.0,0.0,0.0,0.0, 0.0,0.0,0.0,0.0,0.0,0.0]
chasisPos = [0.0,0.0,0.0]
chasisVel = [0.0,0.0,0.0]
gazebo_link_states = 0
referenceFrame = "mmdt_rat20::chasis"
a= 0.2

def quat2eulers(q0, q1, q2, q3):
    """
    Compute yaw-pitch-roll Euler angles from a quaternion.
    
    Args
    ----
        q0: Scalar component of quaternion.
        q1, q2, q3: Vector components of quaternion.
    
    Returns
    -------
        (roll, pitch, yaw) (tuple): 321 Euler angles in radians
    """
    roll = math.atan2(
        2 * ((q2 * q3) + (q0 * q1)),
        q0**2 - q1**2 - q2**2 + q3**2
    )  # radians
    pitch = math.asin(2 * ((q1 * q3) - (q0 * q2)))
    yaw = math.atan2(
        2 * ((q1 * q2) + (q0 * q3)),
        q0**2 + q1**2 - q2**2 - q3**2
    )
    return (roll, pitch, yaw)

def callback(data):
    global frameCommands
    # rospy.loginfo(rospy.get_caller_id() + " I heard %s ", data)
    frameCommands = data.data

def callback_joints(data):
    global robotPos
    global robotVel
    # rospy.loginfo(rospy.get_caller_id() + " I heard %s ", data)
    robotPos = data.position
    robotVel = data.velocity

def callback_gazeboLinks(data):
    global chasisPos
    global chasisVel
    global a
    identChasis= 4      # Este es el identificador para seleccionar el comportamiento del robot en el mundo de gazebo

    referencia= data.name[identChasis]
    # print("Lo que lee: ",referencia)
    # print("Lo que quiero que compare",referenceFrame)
    # print(referencia==referenceFrame)

    # --- Calculo de las posiciones, orientaciones y velocidades del robot respecto al FRAME movil
    chasisPos_X= data.pose[identChasis].position.x
    chasisPos_Y= data.pose[identChasis].position.y
    quaterW= data.pose[identChasis].orientation.w
    quaterX= data.pose[identChasis].orientation.x 
    quaterY= data.pose[identChasis].orientation.y
    quaterZ= data.pose[identChasis].orientation.z 
    euler= quat2eulers(quaterW, quaterZ, quaterY, quaterX)
    orient= euler[0]
    signo=1
    if orient<0:
        signo=-1

    orient= -signo*(math.pi-signo*orient)
    chasisPos= [chasisPos_X, chasisPos_Y, orient]

    chasisVel_W_X= data.twist[identChasis].linear.x 
    chasisVel_W_Y= data.twist[identChasis].linear.y
    chasisVel_W_w= data.twist[identChasis].angular.z
    vels = [chasisVel_W_X, chasisVel_W_Y, chasisVel_W_w]
    velsArr= np.array(vels)
    JacChasis= [[math.cos(orient),-math.sin(orient),-a*math.sin(a+orient)], [math.sin(orient), math.cos(orient), a*math.cos(a+orient)], [0,0,1]]
    invJac= np.linalg.inv(JacChasis)
    chasisVel= invJac.dot(velsArr)
    # print(chasisVel)
    

def talker():
    rospy.init_node('mmdt_talker', anonymous=True)
    pubDerF = rospy.Publisher('/mmdt_rat20/jointDerF_effort/command', Float64, queue_size=10)
    pubDerT = rospy.Publisher('/mmdt_rat20/jointDerT_effort/command', Float64, queue_size=10)
    pubIzqF = rospy.Publisher('/mmdt_rat20/jointIzqF_effort/command', Float64, queue_size=10)
    pubIzqT = rospy.Publisher('/mmdt_rat20/jointIzqT_effort/command', Float64, queue_size=10)

    MMDT_pos = rospy.Publisher('MMDT_pos', Float64MultiArray, queue_size=10)
    MMDT_vel = rospy.Publisher('MMDT_vels', Float64MultiArray, queue_size=10)

    rospy.Subscriber("MMDT_frameCommands", Float64MultiArray, callback)
    rospy.Subscriber("/mmdt_rat20/joint_states", JointState, callback_joints)
    rospy.Subscriber("/gazebo/link_states", LinkStates, callback_gazeboLinks)

    robotPositions = Float64MultiArray()
    robotVelocities = Float64MultiArray()

    rate = rospy.Rate(100) # 10hz
    print('Ejecutando...')
    while not rospy.is_shutdown():       
        # Aplicacion de comandos sobre el robot en GAZEBO
        ruedaDerF= frameCommands[0]
        ruedaDerT= frameCommands[1]
        ruedaIzqF= frameCommands[2]
        ruedaIzqT= frameCommands[3]
        pubDerF.publish(ruedaDerF)
        pubDerT.publish(ruedaDerT)
        pubIzqF.publish(ruedaIzqF)
        pubIzqT.publish(ruedaIzqT)

        # Publicacion de informacion para consumir en MATLAB    
        # print(frameCommands)
        robotPositions.data= tuple(chasisPos)+tuple(robotPos[4:18])
        robotVelocities.data= tuple(chasisVel)+tuple(robotVel[4:18])

        MMDT_pos.publish(robotPositions)
        MMDT_vel.publish(robotVelocities)

        rate.sleep()
    print('Terminado!')

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass