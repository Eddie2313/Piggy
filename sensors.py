import time
from sensors import UltrasonicSensor

# Definition of motor pins
LEFT_MOTOR = 9
RIGHT_MOTOR = 10

# Sensor pins
TRIG_L = 2
ECHO_L = 3
TRIG_R = 4
ECHO_R = 5

# Create sensor objects
leftSensor = UltrasonicSensor(TRIG_L, ECHO_L)
rightSensor = UltrasonicSensor(TRIG_R, ECHO_R)


def setup():
    Serial.begin(9600)
    pinMode(LEFT_MOTOR, OUTPUT)
    pinMode(RIGHT_MOTOR, OUTPUT)


def loop():
    distance_L = leftSensor.readDistance()
    distance_R = rightSensor.readDistance()

    # sensor-motor implementation

    if distance_R > distance_L:
        # turn left
        analogWrite(LEFT_MOTOR, 80)
        analogWrite(RIGHT_MOTOR, 120)

    elif distance_L > distance_R:
        # turn right
        analogWrite(LEFT_MOTOR, 120)
        analogWrite(RIGHT_MOTOR, 80)

    elif distance_L == distance_R and (distance_L != 999 and distance_R != 999):
        # move forward
        analogWrite(LEFT_MOTOR, 120)
        analogWrite(RIGHT_MOTOR, 120)

    else:
        # stop
        analogWrite(LEFT_MOTOR, 0)
        analogWrite(RIGHT_MOTOR, 0)


def main():
    setup()
    while True:
        loop()
        time.sleep(0.1)  # equivalent to delay(100)


if __name__ == "__main__":
    main()