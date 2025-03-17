from time import sleep
from pyLoRaRFM9x import LoRa

# 핀 설정
CS_PIN = 8  # SPI CS 핀 (BCM 번호, GPIO8)
RESET_PIN = 25  # 리셋 핀 (BCM 번호, GPIO25)

# LoRa 설정
FREQUENCY = 915.0  # 주파수 (MHz)
TX_POWER = 23  # 송신 출력 (dBm)

# LoRa 객체 생성
lora = LoRa(bcm_pin_cs=CS_PIN, bcm_pin_reset=RESET_PIN, frequency=FREQUENCY, tx_power=TX_POWER)

def receive_data():
    print("LoRa Receiver is started and waiting for data...")
    try:
        while True:
            if lora.received_packet():  # 패킷 수신 여부 확인
                payload = lora.read_payload()  # 수신 데이터 읽기
                print(f"Received: {payload.decode('utf-8')}")
            sleep(0.1)  # 루프 지연
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally:
        lora.close()  # LoRa 객체 종료

if __name__ == "__main__":
    receive_data()
