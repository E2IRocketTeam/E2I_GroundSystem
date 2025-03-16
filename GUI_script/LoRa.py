from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD

# SPI 핀 초기화
BOARD.setup()

class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def start(self):
        self.set_freq(915.0)  # 주파수 설정
        self.set_pa_config(pa_select=1)
        self.set_spreading_factor(7)
        self.set_bw(7)  # Bandwidth 설정 (7=125kHz)
        self.set_coding_rate(4)
        self.set_preamble(8)
        self.set_mode(MODE.RXCONT)  # 수신 모드로 설정
        print("LoRa Receiver started...")
    
    def on_rx_done(self):
        self.set_mode(MODE.STDBY)
        print("\nReceived message: {}".format(self.read_payload(nocheck=True)))
        self.set_mode(MODE.RXCONT)  # 계속 수신하도록 설정

try:
    lora = LoRaRcvCont(verbose=False)
    lora.start()

    while True:
        sleep(1)  # 계속 루프 돌면서 데이터 수신 대기
except KeyboardInterrupt:
    print("Program interrupted by user")
finally:
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
