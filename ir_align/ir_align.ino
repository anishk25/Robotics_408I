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

// M1: right
// M2 : left

void setup() {
  Serial.begin(9600);
  pinMode(POWER_PIN_RIGHT_WHEEL,OUTPUT);
  digitalWrite(POWER_PIN_RIGHT_WHEEL, HIGH);

  pinMode(POWER_PIN_LEFT_WHEEL,OUTPUT);
  digitalWrite(POWER_PIN_LEFT_WHEEL, HIGH);
  motorShield.init();

  //motorShield.setM1Speed(DEFAULT_MOTOR_SPEED);
  //motorShield.setM2Speed(-DEFAULT_MOTOR_SPEED);
  
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

    Serial.print("left:");
    Serial.print(left_ir_value);
    Serial.print("\t");
    Serial.print("right:");
    Serial.println(right_ir_value);

    
    if(right_ir_value > IR_THRESHOLD && left_ir_value > IR_THRESHOLD){
      // stop rotating
      motorShield.setM1Speed(DEFAULT_MOTOR_SPEED-50);
      motorShield.setM2Speed(DEFAULT_MOTOR_SPEED-50);
    }else if(right_ir_value < IR_THRESHOLD && left_ir_value < IR_THRESHOLD){
       motorShield.setM1Speed(rotate_direction * DEFAULT_MOTOR_SPEED);
       motorShield.setM2Speed(rotate_direction *-DEFAULT_MOTOR_SPEED);
    }else{
       int error = right_ir_value - left_ir_value;
       if(error > 0){
          rotate_direction = ROTATE_RIGHT;
       }else{
          rotate_direction = ROTATE_LEFT;
       }
       int motor_speed = error * wheelPowerGain;
       motorShield.setM1Speed(-motor_speed);
       motorShield.setM2Speed(motor_speed);
    }
    //Serial.print("motor speed after:");
    //Serial.println(motor_speed);
    delay(20);
}





