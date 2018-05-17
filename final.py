from envirophat import motion
from math import acos
from math import atan2
from math import hypot
from math import fabs
from math import sqrt
from math import pi
from math import degrees
import time
import serial

carX = 1.0
carY = 1.0
destX = 2.0
destY = 2.0
complete = 0

#These angles will be clockwise from North
angleCar = 0.0
angleTarget = 0.0

vectorX = destX - carX
vectorY = destY - carY
distance = hypot(vectorX, vectorY) * 111699
motion.update()

def findAngles():
    carX = getCoordinateX()
    carY = getCoordinateY()
    angleCar = motion.heading()
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


def getCoordinateX():
    return 0
    #insert code to receive Lora coordinates from other Pi.
    
def getCoordinateY():
    return 0
    #insert code to receive Lora coordinates from other Pi.

#ser = serial.Serial("/dev/ttyACM0",9600)
#ser.flushInput()

while complete == 0:
    
    findAngles()
    
    if angleTarget - angleCar > 0:
        while fabs(angleTarget - angleCar) > 5:
            print("Rotating Right by " + fabs(angleTarget - angleCar) + " degrees.")
            #Implement right rotation code here
            #ser.write("right")
            findAngles()
    elif angleTarget - angleCar < 0:
        while fabs(angleTarget - angleCar) > 5:
            print("Rotating Left by " + fabs(angleTarget-angleCar) + " degrees.")
            #Implement left rotation code here
            #ser.write("left")
            findAngles()
    carX = getCoordinateX()
    carY = getCoordinateY()
    vectorX = destX - carX
    vectorY = destY - carY
    distance = hypot(vectorX, vectorY) * 111699
    if distance > 0.5:
        print("Moving Forward by " + distance + " meters.")
        #Implement forward movement for small duration
        #ser.write("forward")
    else:
        complete = 1