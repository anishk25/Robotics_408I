#include <Encoder.h>
#include <DualMC33926MotorShield.h>

Encoder rightWheel(2,4);
DualMC33926MotorShield motorShield;

long right_wheel_pos = -999;

void setup() {
  Serial.begin(9600);
  rightWheel.write(0);
  // assuming M2 is right wheel
  motorShield.setM2Speed(100);
}

void loop() {
  // put your main code here, to run repeatedly:

}

void readEncoder(){
  long new_right_pos = rightWheel.read();
  if(new_right_pos != new_right_pos){
     right_wheel_pos = new_right_pos;
     Serial.println(right_wheel_pos);
  }
}
