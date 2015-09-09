#include <Encoder.h>
#include <DualMC33926MotorShield.h>

#define COUNTS_PER_REV 4480 // (gear_ratio * 64)

Encoder leftWheel(2,4);
Encoder righWheel(3,5);

DualMC33926MotorShield motorShield;

long left_wheel_pos = -999;
long right_wheel_pos = -999;

float num_left_revs = 0;
float num_right_revs = 0;

void setup() {
   Serial.begin(9600);
   leftWheel.write(0);
   rightWheel.write(0);
}

void loop() {
  if (Serial.available()) {
    Serial.read();
    Serial.println("Reset wheel to zero");
    wheel.write(0);
    wheel.write(0);
  }
  readEncoder();
  
}


void readEncoder(){
  long new_left_pos = leftWheel.read();
  long new_right_pos = rightWheel.read();

  if(new_left_pos != left_wheel_pos || new_right_pos != right_wheel_pos){
     left_wheel_pos = new_left_pos;
     right_wheel_pos = new_right_pos;
     num_left_revs = ((float)left_wheel_pos)/COUNTS_PER_REV;
     num_right_revs = ((float)right_wheel_pos)/COUNTS_PER_REV;
  }
}

