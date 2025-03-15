import board
import busio
import digitalio
import adafruit_rfm9x

# SPI 인터페이스 설정
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# RFM95W 핀 설정
cs = digitalio.DigitalInOut(board.CE0)  # GPIO8
reset = digitalio.DigitalInOut(board.D25)  # GPIO25

# RFM95W 모듈 초기화
try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)  # 주파수 915MHz
    rfm9x.tx_power = 23  # 송신 전력 설정 (최대 23dBm)
    print("LoRa 수신기 시작...")
except Exception as e:
    print(f"LoRa 모듈 초기화 실패: {e}")
    exit()

# 수신 루프
while True:
    packet = rfm9x.receive()  # 패킷 수신
    if packet is not None:
        received_text = str(packet, "utf-8")
        rssi = rfm9x.rssi
        print(f"수신된 데이터: {received_text} | 신호 강도 (RSSI): {rssi} dBm")
