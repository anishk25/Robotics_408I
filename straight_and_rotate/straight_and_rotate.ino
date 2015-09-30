#include <Encoder.h>
#include <DualMC33926MotorShield.h>

#define POWER_PIN_RIGHT_WHEEL 8
#define POWER_PIN_LEFT_WHEEL 9
#define COUNTS_PER_REV 4480

#define MASTER_STRAIGHT_POWER 250
#define MASTER_ROTATE_POWER 200

#define RIGHT_WHEEL_PIN1 2
#define RIGHT_WHEEL_PIN2 6
#define LEFT_WHEEL_PIN1 3
#define LEFT_WHEEL_PIN2 5

enum DriveMode{STRAIGHT,ROTATE_RIGHT,ROTATE_LEFT};

const int kp = 4;
int slavePower = MASTER_STRAIGHT_POWER;

// M1: right
// M2 : left
// master: right/M1
// slave: left/M2

long right_wheel_pos = -999;
long left_wheel_pos = -999;

DualMC33926MotorShield motorShield;

DriveMode mode = ROTATE_RIGHT;
bool modeSwitchOccurred = true;

Encoder rightWheel(2,6);
Encoder leftWheel(3,5);


void setup(){
  pinMode(POWER_PIN_RIGHT_WHEEL,OUTPUT);
  digitalWrite(POWER_PIN_RIGHT_WHEEL, HIGH);

  pinMode(POWER_PIN_LEFT_WHEEL,OUTPUT);
  digitalWrite(POWER_PIN_LEFT_WHEEL, HIGH);

  motorShield.init();
  resetEncoders();
  
}
void loop() {
  switch(mode){
    case STRAIGHT:
        moveStraight();
    case ROTATE_RIGHT:
        rotateRightInPlace();
    case ROTATE_LEFT:
        rotateLeftInPlace();
  }
  readEncoders();
}

void moveStraight(){
  if(modeSwitchOccurred){
      resetEncoders();
      motorShield.setM1Speed(MASTER_STRAIGHT_POWER);
      slavePower = MASTER_STRAIGHT_POWER;
      modeSwitchOccurred = false;
  }
  int error = right_wheel_pos - left_wheel_pos;
  slavePower -= error/kp;
  motorShield.setM2Speed(slavePower);
  resetEncoders();
  delay(100);
}

void rotateRightInPlace(){
  if(modeSwitchOccurred){
    motorShield.setM1Speed(-MASTER_ROTATE_POWER);
    motorShield.setM2Speed(MASTER_ROTATE_POWER);
    modeSwitchOccurred = false;
  }
}

void rotateLeftInPlace(){
  if(modeSwitchOccurred){
    motorShield.setM1Speed(MASTER_ROTATE_POWER);
    motorShield.setM2Speed(-MASTER_ROTATE_POWER);
    modeSwitchOccurred = false;
  }
}


void resetEncoders(){
  rightWheel.write(0);
  leftWheel.write(0);
  right_wheel_pos = 0;
  left_wheel_pos = 0;
}


void readEncoders(){
  long new_right_pos = rightWheel.read();
  long new_left_pos = leftWheel.read();
  
  if(new_right_pos != right_wheel_pos || new_left_pos != left_wheel_pos){
     right_wheel_pos = new_right_pos;
     left_wheel_pos = new_left_pos;
  }
}








