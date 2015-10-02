#include <Encoder.h>
#include <DualMC33926MotorShield.h>

#define POWER_PIN_RIGHT_WHEEL 8
#define POWER_PIN_LEFT_WHEEL 9
#define COUNTS_PER_REV 4480

Encoder rightWheel(2,6);
Encoder leftWheel(3,5);


DualMC33926MotorShield motorShield;

long right_wheel_pos = -999;
long left_wheel_pos = -999;
float right_num_revs = 0;
float left_num_revs = 0;

void setup() {
  Serial.begin(115200);
  //rightWheel.write(0);
  pinMode(POWER_PIN_RIGHT_WHEEL,OUTPUT);
  digitalWrite(POWER_PIN_RIGHT_WHEEL, HIGH);

  pinMode(POWER_PIN_LEFT_WHEEL,OUTPUT);
  digitalWrite(POWER_PIN_LEFT_WHEEL, HIGH);
  
  //M1 is right, M2 is left
  motorShield.init();
  motorShield.setM1Speed(100);
  motorShield.setM2Speed(100);
}

void loop() {
  // put your main code here, to run repeatedly:
  readEncoder();
}

void readEncoder(){
  long new_right_pos = rightWheel.read();
  long new_left_pos = leftWheel.read();
  
  if(new_right_pos != right_wheel_pos || new_left_pos != left_wheel_pos){
     right_wheel_pos = new_right_pos;
     right_num_revs = (float)right_wheel_pos/COUNTS_PER_REV;

     left_wheel_pos = new_left_pos;
     left_num_revs =  (float)left_wheel_pos/COUNTS_PER_REV;

     Serial.print(right_num_revs);
     Serial.print("\t");
     Serial.println(left_num_revs);

  }
}
