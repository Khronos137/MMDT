#!/usr/bin/env python

# Esta version incluye a todos los elementos movibles: 2 latas, 2 mesas y 1 esfera
# Esta version detecta colisiones

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
global referenceFrameChasis
global referenceEndLinkDer
global chasisPos
global chasisVel
global objetosPos
global objetosPos_ant
global a                # Distancia desde el CDG hacia el punto de interes
global identChasis
global identEndLinkDer
global frameCommands_ant

# robotPos = [platfPosX, platfPosY, orient, torsPosZ, torsPosY, manDerQ1..Q6, manIzqQ1..Q6]
# robotVel = [platfVelX, platfVelY, w, torsVelZ, torsVelY, manDerQ1_p..Q6_p, manIzqQ1_p..Q6_p]

frameCommands = [0.0,0.0,0.0,0.0, 0.0,0.0, 0.0,0.0,0.0,0.0,0.0,0.0, 0.0,0.0,0.0,0.0,0.0,0.0]
frameCommands_ant = [0.0,0.0,0.0,0.0, 0.0,0.0, 0.0,0.0,0.0,0.0,0.0,0.0, 0.0,0.0,0.0,0.0,0.0,0.0]
robotPos = [0.0,0.0,0.0, 0.0,0.0, 0.0,0.0,0.0,0.0,0.0,0.0, 0.0,0.0,0.0,0.0,0.0,0.0]  
robotVel = [0.0,0.0,0.0, 0.0,0.0, 0.0,0.0,0.0,0.0,0.0,0.0, 0.0,0.0,0.0,0.0,0.0,0.0]
chasisPos = [0.0,0.0,0.0]
chasisVel = [0.0,0.0,0.0]
objetosPos = [0.0,0.0,0.0, 0.0,0.0,0.0, 0.0,0.0,0.0]
objetosPos_ant = [0.0,0.0,0.0, 0.0,0.0,0.0, 0.0,0.0,0.0]
gazebo_link_states = 0
referenceFrameChasis = "mmdt_rat20::chasis"
referenceEndLinkDer = "mmdt_rat20::end_link_manipDer"
a= 0.2
identChasis= 10000
identEndLinkDer= 10000

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

def callbackObjetos(data):
    global objetosPos
    # rospy.loginfo(rospy.get_caller_id() + " I heard %s ", data)
    objetosPos = data.data

def callback_joints(data):
    global robotPos
    global robotVel
    # rospy.loginfo(rospy.get_caller_id() + " I heard %s ", data)
    robotPos = data.position
    robotVel = data.velocity

def callback_collision(data):
    print("Se choooooocoooooooooo!")

def callback_gazeboLinks(data):
    global chasisPos
    global chasisVel
    global a
    global identChasis
    global identEndLinkDer
    global referenceFrameChasis
    global referenceEndLinkDer

# Identificador del chasis
    if identChasis==10000:
        print("longitud", len(data.pose))
        for kI in range(len(data.pose)):
            referencia= data.name[kI]
            if referencia==referenceFrameChasis:
                print("Referencia de chasis encontrada en: ",kI)
                identChasis=kI
                break
        print("Deberia ser la de chasis: ", data.name[identChasis],identChasis)

    if identEndLinkDer==10000:
        print("longitud", len(data.pose))
        for kI in range(len(data.pose)):
            referencia= data.name[kI]
            if referencia==referenceEndLinkDer:
                print("Referencia de EndLink encontrada en: ",kI)
                identEndLinkDer=kI
                break
        print("Deberia ser la de EndLink: ", data.name[identEndLinkDer],identEndLinkDer)

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

    # print(data.name[identEndLinkDer])
    # print(data.pose[identEndLinkDer].position)

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
    global frameCommands_ant
    global objetosPos_ant

    rospy.init_node('mmdt_talker', anonymous=True)
    pubDerF = rospy.Publisher('/mmdt_rat20/jointDerF_effort/command', Float64, queue_size=10)
    pubDerT = rospy.Publisher('/mmdt_rat20/jointDerT_effort/command', Float64, queue_size=10)
    pubIzqF = rospy.Publisher('/mmdt_rat20/jointIzqF_effort/command', Float64, queue_size=10)
    pubIzqT = rospy.Publisher('/mmdt_rat20/jointIzqT_effort/command', Float64, queue_size=10)

    pubBaseTorso = rospy.Publisher('/mmdt_rat20/jointBaseTorso_position/command', Float64, queue_size=10)
    pubTorso = rospy.Publisher('/mmdt_rat20/jointTorso_position/command', Float64, queue_size=10)

    pubDer1 = rospy.Publisher('/mmdt_rat20/joint1_manipDer_position/command', Float64, queue_size=10)
    pubDer2 = rospy.Publisher('/mmdt_rat20/joint2_manipDer_position/command', Float64, queue_size=10)
    pubDer3 = rospy.Publisher('/mmdt_rat20/joint3_manipDer_position/command', Float64, queue_size=10)
    pubDer4 = rospy.Publisher('/mmdt_rat20/joint4_manipDer_position/command', Float64, queue_size=10)
    pubDer5 = rospy.Publisher('/mmdt_rat20/joint5_manipDer_position/command', Float64, queue_size=10)
    pubDer6 = rospy.Publisher('/mmdt_rat20/joint6_manipDer_position/command', Float64, queue_size=10)

    pubIzq1 = rospy.Publisher('/mmdt_rat20/joint1_manipIzq_position/command', Float64, queue_size=10)
    pubIzq2 = rospy.Publisher('/mmdt_rat20/joint2_manipIzq_position/command', Float64, queue_size=10)
    pubIzq3 = rospy.Publisher('/mmdt_rat20/joint3_manipIzq_position/command', Float64, queue_size=10)
    pubIzq4 = rospy.Publisher('/mmdt_rat20/joint4_manipIzq_position/command', Float64, queue_size=10)
    pubIzq5 = rospy.Publisher('/mmdt_rat20/joint5_manipIzq_position/command', Float64, queue_size=10)
    pubIzq6 = rospy.Publisher('/mmdt_rat20/joint6_manipIzq_position/command', Float64, queue_size=10)

    latitaCervX = rospy.Publisher('/latitaCerveza/cervezaX_controller/command', Float64, queue_size=10)
    latitaCervY = rospy.Publisher('/latitaCerveza/cervezaY_controller/command', Float64, queue_size=10)
    latitaCervZ = rospy.Publisher('/latitaCerveza/cervezaZ_controller/command', Float64, queue_size=10)

    latitaObjX = rospy.Publisher('/latitaObjetivo/latitaObjX_controller/command', Float64, queue_size=10)
    latitaObjY = rospy.Publisher('/latitaObjetivo/latitaObjY_controller/command', Float64, queue_size=10)
    latitaObjZ = rospy.Publisher('/latitaObjetivo/latitaObjZ_controller/command', Float64, queue_size=10)

    esferaX = rospy.Publisher('/esferaIndic/esferaX_controller/command', Float64, queue_size=10)
    esferaY = rospy.Publisher('/esferaIndic/esferaY_controller/command', Float64, queue_size=10)
    esferaZ = rospy.Publisher('/esferaIndic/esferaZ_controller/command', Float64, queue_size=10)

    MMDT_pos = rospy.Publisher('/MMDT_pos', Float64MultiArray, queue_size=10)
    MMDT_vel = rospy.Publisher('/MMDT_vels', Float64MultiArray, queue_size=10)

    rospy.Subscriber("/MMDT_frameCommands", Float64MultiArray, callback)
    rospy.Subscriber("/objetos_position", Float64MultiArray, callbackObjetos)
    rospy.Subscriber("/mmdt_rat20/joint_states", JointState, callback_joints)
    rospy.Subscriber("/gazebo/link_states", LinkStates, callback_gazeboLinks)
    # rospy.Subscriber("/gazebo/default/grey_wallFront/link/my_contact", Contacts, callback_collision)

    robotPositions = Float64MultiArray()
    robotVelocities = Float64MultiArray()

    rate = rospy.Rate(100) # 10hz
    print('Ejecutando...')
    print('Inicia simulacion en Gazebo!')
    while not rospy.is_shutdown():       
        # Aplicacion de comandos sobre el robot en GAZEBO

        vectCompFrameAll= np.array_equal(frameCommands,frameCommands_ant) # Compara vectores para ver si hay cambios, 0: no

        if vectCompFrameAll==0:                 # Si 0, los vectores han cambiado!
            ruedaDerF= frameCommands[0]
            ruedaDerT= frameCommands[1]
            ruedaIzqF= frameCommands[2]
            ruedaIzqT= frameCommands[3]
            BaseTorso= frameCommands[4]
            Torso= frameCommands[5]
            der1= frameCommands[6]
            der2= frameCommands[7]
            der3= frameCommands[8]
            der4= frameCommands[9]
            der5= frameCommands[10]
            der6= frameCommands[11]
            izq1= frameCommands[12]
            izq2= frameCommands[13]
            izq3= frameCommands[14]
            izq4= frameCommands[15]
            izq5= frameCommands[16]
            izq6= frameCommands[17]

            vecCompFrameEachF= np.array(frameCommands)==np.array(frameCommands_ant)  # Compara elemento por elemento

            if vecCompFrameEachF[0]==0:
                pubDerF.publish(ruedaDerF)
            if vecCompFrameEachF[1]==0:
                pubDerT.publish(ruedaDerT)
            if vecCompFrameEachF[2]==0:
                pubIzqF.publish(ruedaIzqF)
            if vecCompFrameEachF[3]==0:
                pubIzqT.publish(ruedaIzqT)

            if vecCompFrameEachF[4]==0:
                pubBaseTorso.publish(BaseTorso)
            if vecCompFrameEachF[5]==0:
                pubTorso.publish(Torso)

            if vecCompFrameEachF[6]==0:
                pubDer1.publish(der1)
            if vecCompFrameEachF[7]==0:
                pubDer2.publish(der2)
            if vecCompFrameEachF[8]==0:
                pubDer3.publish(der3)
            if vecCompFrameEachF[9]==0:
                pubDer4.publish(der4)
            if vecCompFrameEachF[10]==0:
                pubDer5.publish(der5)
            if vecCompFrameEachF[11]==0:
                pubDer6.publish(der6)

            if vecCompFrameEachF[12]==0:
                pubIzq1.publish(izq1)
            if vecCompFrameEachF[13]==0:
                pubIzq2.publish(izq2)
            if vecCompFrameEachF[14]==0:
                pubIzq3.publish(izq3)
            if vecCompFrameEachF[15]==0:
                pubIzq4.publish(izq4)
            if vecCompFrameEachF[16]==0:
                pubIzq5.publish(izq5)
            if vecCompFrameEachF[17]==0:
                pubIzq6.publish(izq6)

        vectCompObj= np.array_equal(objetosPos,objetosPos_ant) # Compara vectores para ver si hay cambios, 0: no
        if vectCompObj==0:                 # Si 0, los vectores han cambiado!

            cervX= objetosPos[0]
            cervY= objetosPos[1]
            cervZ= objetosPos[2]
            objX= objetosPos[3]
            objY= objetosPos[4]
            objZ= objetosPos[5]
            esfX= objetosPos[6]
            esfY= objetosPos[7]
            esfZ= objetosPos[8]

            vecCompFrameEach= np.array(objetosPos)==np.array(objetosPos_ant)  # Compara elemento por elemento

            if vecCompFrameEach[0]==0:
                latitaCervX.publish(cervX)
            if vecCompFrameEach[1]==0:
                latitaCervY.publish(cervY)
            if vecCompFrameEach[2]==0:
                latitaCervZ.publish(cervZ)

            if vecCompFrameEach[3]==0:
                latitaObjX.publish(objX)
            if vecCompFrameEach[4]==0:
                latitaObjY.publish(objY)
            if vecCompFrameEach[5]==0:
                latitaObjZ.publish(objZ)

            if vecCompFrameEach[6]==0:
                esferaX.publish(esfX)
            if vecCompFrameEach[7]==0:
                esferaY.publish(esfY)
            if vecCompFrameEach[8]==0:
                esferaZ.publish(esfZ)

        # Publicacion de informacion para consumir en MATLAB    
        # print(frameCommands)
        robotPositions.data= tuple(chasisPos)+tuple(robotPos[4:18])
        robotVelocities.data= tuple(chasisVel)+tuple(robotVel[4:18])

        MMDT_pos.publish(robotPositions)
        MMDT_vel.publish(robotVelocities)

        frameCommands_ant= frameCommands
        objetosPos_ant= objetosPos
        rate.sleep()
    print('Terminado!')

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass