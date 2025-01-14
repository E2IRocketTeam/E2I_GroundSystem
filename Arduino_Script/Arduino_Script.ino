#include <TinyGPS++.h>

// TinyGPS++ 객체 생성
TinyGPSPlus gps;

// 하드웨어 시리얼 포트 설정 (Teensy 4.1의 Serial1 사용)
#define gpsSerial Serial1

void setup() {
  Serial.begin(9600);        // 기본 시리얼 모니터
  gpsSerial.begin(9600);     // BK-880Q 기본 통신 속도
  
  Serial.println("BK-880Q GPS 데이터 수신 준비 완료");
}

void loop() {
  // GPS 데이터 수신 및 파싱
  while (gpsSerial.available()) {
    gps.encode(gpsSerial.read());
    
    // 위치 데이터 업데이트 확인
    if (gps.location.isUpdated()) {
      Serial.print("위도: ");
      Serial.println(gps.location.lat(), 6); // 소수점 6자리까지
      Serial.print("경도: ");
      Serial.println(gps.location.lng(), 6);
      Serial.print("고도: ");
      Serial.println(gps.altitude.meters(), 2); // 고도 출력
      Serial.print("속도: ");
      Serial.println(gps.speed.kmph(), 2); // 속도 출력 (km/h)
    }
  }
}
