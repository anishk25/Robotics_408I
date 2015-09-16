#include <Encoder.h>
#include <DualMC33926MotorShield.h>

#define COUNTS_PER_REV 4480 // (gear_ratio * 64)

Encoder leftWheel(2,4);
Encoder rightWheel(3,5);

DualMC33926MotorShield motorShield;

long left_wheel_pos = -999;
long right_wheel_pos = -999;

float num_left_revs = 0;
float num_right_revs = 0;

const float revs_for_turns = 0.25f;
boolean isMotor1Running = true;
boolean isMotor2Running = true;

void setup() {
   Serial.begin(9600);
   leftWheel.write(0);
   rightWheel.write(0);

   // start motor one goes forward, one goes backward
   motorShield.setM1Speed(-100);
   motorShield.setM2Speed(100);
}

void loop() {
  if (Serial.available()) {
    Serial.read();
    Serial.println("Reset wheel to zero");
    leftWheel.write(0);
    rightWheel.write(0);
  }
  readEncoder();
  checkIfTurnCompleted();
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

void checkIfTurnCompleted(){
   if(isMotor1Running){
      if(num_left_revs)
   }
}



