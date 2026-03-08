#translation from sensor.cpp
#using only one sensor for now
import time
from sensors import UltrasonicSensor
from gpiozero import Motor

#this is how we create motors, the numbers are the pins on the pi
LEFT = Motor(17,27,enable=22,pwm=True)
RIGHT = Motor(23,24,enable=25,pwm=True)

TRIG = 2
ECHO = 3

sensor = UltrasonicSensor(TRIG, ECHO)

def loop():

    distance = sensor.readDistance()

    print("Distance:", distance)
    if distance > 30:
        # nothing close → move forward
        LEFT.forward(0.6)
        RIGHT.forward(0.6)

    elif distance < 15:
        # obstacle close → turn
        LEFT.forward(0.6)
        RIGHT.backward(0.6)

    else:
        # medium distance → slow forward
        LEFT.forward(0.3)
        RIGHT.forward(0.3)

while True:
    loop()
    time.sleep(0.1)