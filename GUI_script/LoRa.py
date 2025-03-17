from time import sleep
from SX127x.LoRa import LoRa, MODE
from SX127x.board_config import BOARD

# Raspberry Pi 핀 구성 초기화
BOARD.setup()

class LoRaReceiver(LoRa):
    def __init__(self, verbose=False):
        super(LoRaReceiver, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def start(self):
        self.set_freq(915.0)  # Teensy 송신 코드와 동일한 주파수 설정
        self.set_pa_config(pa_select=1)
        self.set_spreading_factor(7)  # Spreading Factor 설정
        self.set_bw(7)  # Bandwidth (125kHz)
        self.set_coding_rate(5)  # Coding Rate (4/5)
        self.set_preamble(8)  # Preamble 길이
        self.set_mode(MODE.RXCONT)  # Continuous RX 모드
        print("LoRa Receiver is started and waiting for incoming data...")

    def on_rx_done(self):
        self.set_mode(MODE.STDBY)
        payload = self.read_payload(nocheck=True)
        print(f"Received data: {payload.decode('utf-8')}")
        self.set_mode(MODE.RXCONT)  # 다시 수신 모드로 설정

# LoRaReceiver 객체 생성
try:
    lora = LoRaReceiver(verbose=False)
    lora.start()

    while True:
        sleep(1)  # 계속 데이터를 대기
except KeyboardInterrupt:
    print("Program interrupted by user.")
finally:
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
