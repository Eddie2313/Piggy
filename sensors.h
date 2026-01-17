#pragma once
#include <Arduino.h>


// class definition
class UltrasonicSensor{
    public:
    UltrasonicSensor(int t, int e);
    long readDistance();

    private:
    int trigPin;
    int echoPin;
};

// class implementation
// This function below determines the distance between the object and the sensors.
long UltrasonicSensor::readDistance(){
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    long duration = pulseIn(echoPin, HIGH, 30000);
    // checks for whether an object is detected (if it's not there, too close, or too far this is returned)
    if(duration == 0)
        return 999;
    return (duration * .034) / 2.0;
}

// Below is a parameterized constructor that deals with the definition of each sensor.
UltrasonicSensor::UltrasonicSensor(int t, int e){
    trigPin = t;
    echoPin = e;
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
}

