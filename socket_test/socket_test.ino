#include <ESP8266.h>
#include <SoftwareSerial.h>

#define WIFI_SSID "Robonet"
#define WIFI_PASS "awesomeness"
#define HOST_NAME "192.168.43.141"
#define HOST_PORT 31415
#define LED_PIN 13

SoftwareSerial wifiSerial(8,9);
ESP8266 wifi(Serial);

char *ping_str = "PING";



void setup() {
   pinMode(LED_PIN,OUTPUT);
   wifi.setOprToStationSoftAP();
   if(wifi.joinAP(WIFI_SSID, WIFI_PASS)){
      digitalWrite(LED_PIN,HIGH);
   }else{
      digitalWrite(LED_PIN,LOW);
   }
   //wifi.disableMUX();
   //wifi.createTCP(HOST_NAME,HOST_PORT);
}

void loop() {
  //wifi.send((const uint8_t*) ping_str, strlen(ping_str));
  //delay(5000);
}
