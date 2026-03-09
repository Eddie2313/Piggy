#trasnlation from sensors.h
import time
#next import is squiggled cus it is raspi preinstalled
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class UltrasonicSensor:

    def __init__(self, trigPin, echoPin):
        self.trigPin = trigPin
        self.echoPin = echoPin

        GPIO.setup(self.trigPin, GPIO.OUT)
        GPIO.setup(self.echoPin, GPIO.IN)

    def readDistance(self):

        GPIO.output(self.trigPin, False)
        time.sleep(0.000002)

        GPIO.output(self.trigPin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigPin, False)

        start = time.time()

        while GPIO.input(self.echoPin) == 0:
            start = time.time()

        while GPIO.input(self.echoPin) == 1:
            stop = time.time()

        duration = stop - start

        distance = duration * 34300 / 2

        if distance == 0:
            return 999

        return distance