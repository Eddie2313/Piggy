#include <Arduino.h>
#include "sensors.h"

// Definition of motor pins. These numbers are also subject to change if necesssary
#define LEFT_MOTOR 9
#define RIGHT_MOTOR 10
UltrasonicSensor leftSensor(TRIG_L, ECHO_L);       
UltrasonicSensor rightSensor(TRIG_R, ECHO_R);

// The numbers here should be changed according to the pins' wiring on the arduino board
const int TRIG_L = 2;
const int ECHO_L = 3;
const int TRIG_R = 4;
const int ECHO_R = 5;

void setup(){
    Serial.begin(9600);
    pinMode(LEFT_MOTOR, OUTPUT);
    pinMode(RIGHT_MOTOR, OUTPUT);
}

void loop(){
    long distance_L = leftSensor.readDistance();
    long distance_R = rightSensor.readDistance();

    // sensor-motor implementation.

    if(distance_R > distance_L){
        // turn left
        analogWrite(LEFT_MOTOR, 80);
        analogWrite(RIGHT_MOTOR, 120);
    } else if (distance_L > distance_R){
        // turn right
        analogWrite(LEFT_MOTOR, 120);
        analogWrite(RIGHT_MOTOR, 80);
    } else if (distance_L == distance_R && (distance_L != 999 && distance_R != 999)){
        // move forward
        analogWrite(LEFT_MOTOR, 120);
        analogWrite(RIGHT_MOTOR, 120);
    } else{
        // stop
        analogWrite(LEFT_MOTOR, 0);
        analogWrite(RIGHT_MOTOR, 0);
    }

    delay(100);  // prevents overflowing
    
}
