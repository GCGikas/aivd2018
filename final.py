#from envirophat import motion
import requests
import gpsd
gpsd.connect()
from math import acos
from math import atan2
from math import hypot
from math import fabs
from math import sqrt
from math import pi
from math import degrees
from math import sin
from math import cos
from math import radians
import time
#import serial

carX = 1.0
carY = 1.0
#(42.301383333, -83.699086667)
destX = 42.301383333
destY = -83.699086667
complete = 0
angleDelta = 0.0

#These angles will be clockwise from North
angleCar = 0.0
angleTarget = 0.0

vectorX = destX - carX
vectorY = destY - carY
distance = hypot(vectorX, vectorY) * 111699

def findAngles():
    global carX
    global carY
    global vectorX
    global vectorY
    global angleCar
    global angleTarget
    global complete
    global angleDelta
    
    posTuple = getPosition()
    carX = posTuple[0]
    carY = posTuple[1]
    #angleCar = motion.heading()
    angleCar = float(requests.get('http://10.1.1.2/').text)
    print('car angle: ' + str(angleCar))
    vectorX = destX - carX
    vectorY = destY - carY
    if vectorX > 0:
        if vectorY > 0:
            angleTarget = 90 - degrees(atan2(vectorX, vectorY))
        elif vectorY < 0:
            angleTarget = 90 + degrees(atan2(vectorX, vectorY))
        else:
            angleTarget = 90
    elif vectorX < 0:
        if vectorY != 0:
            angleTarget = 270 - degrees(atan2(vectorX, vectorY))
        else:
            angleTarget = 270
    else:
        if vectorY > 0:
            angleTarget =0
        elif vectorY < 0:
            angleTarget = 180
        else:
            complete = 1
    angleDelta = degrees(atan2(sin(radians(angleTarget)-radians(angleCar)), cos(radians(angleTarget)-radians(angleCar))))


def getPosition():
    packet = gpsd.get_current()
    return packet.position()

#ser = serial.Serial("/dev/ttyACM0",9600)
#ser.flushInput()

while complete == 0:
    
    findAngles()
    
    print("target angle: " + str(angleTarget))
    if angleDelta>0:
        #clockwise
        while fabs(angleDelta) > 10:
            print("Rotating Right by " + str(angleDelta) + " degrees.")
            #Implement right rotation code here
            #ser.write("right")
            findAngles()
            print("target angle: " + str(angleTarget))
            time.sleep(1)
    else:
        #counterclockwise
        while fabs(angleDelta) > 10:
            print("Rotating Left by " + str(angleDelta) + " degrees.")
            #Implement left rotation code here
            #ser.write("left")
            findAngles()
            print("target angle: " + str(angleTarget))
            time.sleep(1)
    posTuple = getPosition()
    carX = posTuple[0]
    carY = posTuple[1]
    vectorX = destX - carX
    vectorY = destY - carY
    distance = hypot(vectorX, vectorY) * 111699
    print("distance from dest: " + str(distance))
    if distance > 3:
        print("Moving Forward by " + str(distance) + " meters.")
        time.sleep(1)
        #Implement forward movement for small duration
        #ser.write("forward")
    else:
        complete = 1
