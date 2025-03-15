import spidev
import RPi.GPIO as GPIO
import time

# LoRa 모듈의 SPI 연결 핀 설정
LORA_RST = 25  # LoRa 리셋 핀 (GPIO25)
LORA_CS = 8    # LoRa 칩 선택 핀 (GPIO8)

# SPI 인터페이스 설정
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI 버스 0, 장치 0 (CE0)
spi.max_speed_hz = 5000000  # 최대 속도 5MHz

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(LORA_RST, GPIO.OUT)
GPIO.setup(LORA_CS, GPIO.OUT)

# LoRa 모듈 리셋 함수
def reset_lora():
    GPIO.output(LORA_RST, GPIO.LOW)
    time.sleep(0.01)
    GPIO.output(LORA_RST, GPIO.HIGH)
    time.sleep(0.01)

# SPI를 통해 SX127x 레지스터 읽기 함수
def spi_read(register):
    GPIO.output(LORA_CS, GPIO.LOW)
    response = spi.xfer2([register & 0x7F, 0x00])  # 첫 바이트는 읽기, 두 번째는 응답값 받기
    GPIO.output(LORA_CS, GPIO.HIGH)
    return response[1]

# LoRa 모듈 연결 확인
def check_lora_connection():
    reset_lora()
    version = spi_read(0x42)  # WHO_AM_I (Version) 레지스터 읽기

    if version == 0x12:  # SX1276/SX1278 모듈은 0x12를 반환
        print("OK")
    else:
        print("NO")

# 실행
if __name__ == "__main__":
    try:
        check_lora_connection()
    except KeyboardInterrupt:
        print("\n프로그램 종료")
    finally:
        GPIO.cleanup()
        spi.close()
