import spidev
import RPi.GPIO as GPIO
import time

# 핀 설정
LORA_RST = 25  # LoRa 모듈 리셋 핀 (GPIO25)
LORA_CS = 8    # LoRa 모듈 CS 핀 (GPIO8)
LORA_IRQ = 4   # LoRa 모듈 IRQ 핀 (GPIO4)

# SPI 인터페이스 설정
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI 버스 0, 장치 0 (CE0)
spi.max_speed_hz = 5000000  # 5MHz

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(LORA_RST, GPIO.OUT)
GPIO.setup(LORA_CS, GPIO.OUT)
GPIO.setup(LORA_IRQ, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# LoRa 모듈 리셋 함수
def reset_lora():
    GPIO.output(LORA_RST, GPIO.LOW)
    time.sleep(0.01)
    GPIO.output(LORA_RST, GPIO.HIGH)
    time.sleep(0.01)

# SPI를 통해 SX127x 레지스터 읽기
def spi_read(register):
    GPIO.output(LORA_CS, GPIO.LOW)
    response = spi.xfer2([register & 0x7F, 0x00])
    GPIO.output(LORA_CS, GPIO.HIGH)
    return response[1]

# SPI를 통해 SX127x 레지스터 쓰기
def spi_write(register, value):
    GPIO.output(LORA_CS, GPIO.LOW)
    spi.xfer2([register | 0x80, value])
    GPIO.output(LORA_CS, GPIO.HIGH)

# LoRa 초기화 함수
def init_lora():
    reset_lora()
    
    spi_write(0x01, 0x81)  # LoRa 모드 설정 (Long Range Mode)
    spi_write(0x06, 0x6C)  # 주파수 설정 (915MHz 기준)
    spi_write(0x07, 0x80)
    spi_write(0x08, 0x00)
    
    spi_write(0x1D, 0x72)  # 대역폭(BW), 확산인자(SF), 부호화율(CR) 설정
    spi_write(0x1E, 0x74)  
    spi_write(0x26, 0x04)  # LowDataRateOptimize 활성화
    
    spi_write(0x20, 0x00)  # 프리앰블 길이 설정
    spi_write(0x21, 0x08)
    
    spi_write(0x22, 0x40)  # 패킷 최대 길이
    spi_write(0x40, 0x00)  # 비트 동기화 설정
    
    spi_write(0x0D, 0x00)  # FIFO 포인터 리셋
    spi_write(0x0E, 0x00)
    
    spi_write(0x01, 0x85)  # 수신 모드 활성화 (RX Continuous Mode)

# 수신 데이터 읽기
def receive_packet():
    if GPIO.input(LORA_IRQ) == GPIO.HIGH:
        spi_write(0x12, 0xFF)  # IRQ 클리어
        packet_size = spi_read(0x13)  # 패킷 크기 읽기
        fifo_addr = spi_read(0x10)  # FIFO 시작 주소 읽기
        spi_write(0x0D, fifo_addr)  # FIFO 포인터 설정
        
        payload = []
        for _ in range(packet_size):
            payload.append(spi_read(0x00))  # FIFO에서 데이터 읽기
        
        rssi = spi_read(0x1A) - 157  # RSSI 계산
        print(f"수신된 데이터: {bytes(payload).decode('utf-8', 'ignore')} | 신호 강도: {rssi} dBm")

# 메인 실행 루프
if __name__ == "__main__":
    try:
        init_lora()
        print("LoRa 수신기 시작...")
        
        while True:
            receive_packet()
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("\n종료 중...")
        GPIO.cleanup()
        spi.close()
        print("LoRa 종료 완료")
