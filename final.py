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
import time
#import serial

carX = 1.0
carY = 1.0
destX = 43.30363
destY = -84.688926667
complete = 0

#These angles will be clockwise from North
angleCar = 0.0
angleTarget = 0.0

vectorX = destX - carX
vectorY = destY - carY
distance = hypot(vectorX, vectorY) * 111699

def findAngles():
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


def getPosition():
    packet = gpsd.get_current()
    return packet.position()

#ser = serial.Serial("/dev/ttyACM0",9600)
#ser.flushInput()

while complete == 0:
    
    findAngles()
    
    print(angleTarget)
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
    posTuple = getPosition()
    carX = posTuple[0]
    carY = posTuple[1]
    vectorX = destX - carX
    vectorY = destY - carY
    distance = hypot(vectorX, vectorY) * 111699
    if distance > 0.5:
        print("Moving Forward by " + str(distance) + " meters.")
        #Implement forward movement for small duration
        #ser.write("forward")
    else:
        complete = 1
