#include <Encoder.h>
#include <DualMC33926MotorShield.h>

#define POWER_PIN_RIGHT_WHEEL 8
#define POWER_PIN_LEFT_WHEEL 9
#define COUNTS_PER_REV 4480


const int kp = 4;

// M1: right
// M2 : left
// master: right/M1
// slave: left/M2

int masterPower = 300;
int slavePower = 300;

Encoder rightWheel(2,6);
Encoder leftWheel(3,5);

DualMC33926MotorShield motorShield;

long right_wheel_pos = -999;
long left_wheel_pos = -999;
float right_num_revs = 0;
float left_num_revs = 0;

void setup() {
  pinMode(POWER_PIN_RIGHT_WHEEL,OUTPUT);
  digitalWrite(POWER_PIN_RIGHT_WHEEL, HIGH);

  pinMode(POWER_PIN_LEFT_WHEEL,OUTPUT);
  digitalWrite(POWER_PIN_LEFT_WHEEL, HIGH);
  
  motorShield.init();
  motorShield.setM1Speed(masterPower);
  //motorShield.setM2Speed(slavePower);

  resetEncoders();
}



void loop() {
  readEncoder();
  adjustMotorPowers();
  motorShield.setM2Speed(slavePower);
}

void adjustMotorPowers(){
  int error = right_wheel_pos - left_wheel_pos;
  slavePower -= error/kp;
  resetEncoders();
  delay(100);
}

void resetEncoders(){
  rightWheel.write(0);
  leftWheel.write(0);
  right_wheel_pos = 0;
  left_wheel_pos = 0;
}

void readEncoder(){
  long new_right_pos = rightWheel.read();
  long new_left_pos = leftWheel.read();
  
  if(new_right_pos != right_wheel_pos || new_left_pos != left_wheel_pos){
     right_wheel_pos = new_right_pos;
     right_num_revs = (float)right_wheel_pos/COUNTS_PER_REV;
     left_wheel_pos = new_left_pos;
     left_num_revs =  (float)left_wheel_pos/COUNTS_PER_REV;
  }
}

