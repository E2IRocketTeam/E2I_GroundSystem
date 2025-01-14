#include "MPU9250_asukiaaa.h"

MPU9250_asukiaaa sensor(Wire, 0x68);

void setup() {
  Serial.begin(9600);
  Wire.begin();
  sensor.beginAccel();
}

void loop() {
  sensor.accelUpdate();
  float ax = sensor.accelX();
  float ay = sensor.accelY();
  float az = sensor.accelZ();
  
  Serial.print("AX:");
  Serial.print(ax);
  Serial.print(" AY:");
  Serial.print(ay);
  Serial.print(" AZ:");
  Serial.println(az);

  delay(1000); // 1초 간격으로 전송
}
