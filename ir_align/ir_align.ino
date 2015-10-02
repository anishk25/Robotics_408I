#include <DualMC33926MotorShield.h>

#define POWER_PIN_RIGHT_WHEEL 8
#define POWER_PIN_LEFT_WHEEL 9

#define IR_ANALOG_PIN_LEFT  0
#define IR_ANALOG_PIN_RIGHT 1

#define IR_THRESHOLD 100

#define DEFAULT_MOTOR_SPEED 250

#define IR_MES_LIMIT 100

#define ROTATE_LEFT 1
#define ROTATE_RIGHT -1

const float wheelPowerGain = 0.2;
int left_motor_speed = DEFAULT_MOTOR_SPEED;
int right_motor_speed = DEFAULT_MOTOR_SPEED;

int rotate_direction = ROTATE_LEFT;

DualMC33926MotorShield motorShield;

enum State {ROTATE, MOVE_FORWARD, NONE_SEE};

State currState = ROTATE;
State nextState = ROTATE;

int leftMotorSpeed = DEFAULT_MOTOR_SPEED;
int rightMotorSpeed = -DEFAULT_MOTOR_SPEED;



// M1: right
// M2 : left

void setup() {
  Serial.begin(9600);
  pinMode(POWER_PIN_RIGHT_WHEEL,OUTPUT);
  digitalWrite(POWER_PIN_RIGHT_WHEEL, HIGH);

  pinMode(POWER_PIN_LEFT_WHEEL,OUTPUT);
  digitalWrite(POWER_PIN_LEFT_WHEEL, HIGH);
  motorShield.init();
  
}

void loop() {
  // put your main code here, to run repeatedly:
  followIREmitter();
}


void followIREmitter(){
    long right_ir_value = 0;
    long left_ir_value = 0;

    for(int i = 0; i < IR_MES_LIMIT; i++){
        right_ir_value += analogRead(IR_ANALOG_PIN_RIGHT);
        left_ir_value += analogRead(IR_ANALOG_PIN_LEFT);
    }

    right_ir_value /= IR_MES_LIMIT;
    left_ir_value /= IR_MES_LIMIT;

    currState = nextState;

    switch(currState){
      case ROTATE:
           if(right_ir_value > IR_THRESHOLD && left_ir_value > IR_THRESHOLD){
                nextState = MOVE_FORWARD;
           }else if(right_ir_value < IR_THRESHOLD && left_ir_value < IR_THRESHOLD){
                nextState = NONE_SEE;
           }else{
                int error = right_ir_value - left_ir_value;
                if(error > 0){
                  rotate_direction = ROTATE_RIGHT;
                }else{
                  rotate_direction = ROTATE_LEFT;
                }
                int motor_speed = error * wheelPowerGain;
                leftMotorSpeed = motor_speed;
                rightMotorSpeed = -motor_speed;
           }
           break;
      case MOVE_FORWARD:
                leftMotorSpeed = DEFAULT_MOTOR_SPEED;
                rightMotorSpeed = DEFAULT_MOTOR_SPEED;
                nextState = ROTATE;
                break; 
      case NONE_SEE:
                leftMotorSpeed = rotate_direction * -DEFAULT_MOTOR_SPEED;
                rightMotorSpeed = rotate_direction * DEFAULT_MOTOR_SPEED;
                nextState = ROTATE;
           break;
    }

    motorShield.setM1Speed(rightMotorSpeed);
    motorShield.setM2Speed(leftMotorSpeed);
    delay(1);
}





