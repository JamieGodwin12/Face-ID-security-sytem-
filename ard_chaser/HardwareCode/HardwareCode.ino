#include <Stepper.h>
#define STEPS 2038 //sets the ammount of steps for the step motor in use the 28BYJ-48
Stepper stepper(STEPS, 8, 10, 9, 11);//sets the pins in use on the board
int data, flag = 2;
void setup()
{
     stepper.setSpeed(10);//sets speed of the motor in rotations per minute 
     Serial.begin(9600);//establishes serial communication between Arduino board and pc 
}
void loop()
{
    while (Serial.available()) {
        data = Serial.read();//reads the serial output from python 
        if (data == '1') {
            flag = 1;
            Serial.print("Unlocking\n");//added for testing to see output 
        } else if (data == '0') {
            Serial.print("Not recognised\n");//added for testing to see output 
            flag = 0;
        }
        if (flag == 1) {
            stepper.step(2038);//one full clockwise rotation of motor 
            delay(6000);//waits 6 secounds before locking the door after unlocking
            Serial.print("Locking\n");//added for testing to see output 
            stepper.step(-2038);//one full anticlockwise rotation of motor
            flag =2;
            }
       delay(2000);
    }
}
