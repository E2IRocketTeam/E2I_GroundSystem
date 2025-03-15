import time
from LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import LoRaConstants

# 라즈베리파이 SPI 설정 초기화
BOARD.setup()

class LoRaReceiver(LoRa):
    def __init__(self, verbose=False):
        super(LoRaReceiver, self).__init__(verbose)
        self.set_mode(LoRaConstants.MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.set_freq(915.0)  # LoRa 주파수 설정 (915MHz)
        self.set_spreading_factor(7)  # 확산 인자 (SF7)
        self.set_bandwidth(LoRaConstants.BW.BW125)  # 대역폭 125kHz
        self.set_coding_rate(LoRaConstants.CR.CR4_5)  # 부호화율 4/5
        self.set_preamble(8)  # 프리앰블 길이
        self.set_sync_word(0x12)  # 동기화 워드 설정
        self.set_rx_crc(True)  # CRC 사용

    def on_rx_done(self):
        """ 패킷 수신 이벤트 핸들러 """
        self.clear_irq_flags(LoRaConstants.IRQ_RXDONE)
        payload = self.read_payload(nocheck=True)
        received_data = bytes(payload).decode('utf-8', 'ignore')
        rssi = self.get_pkt_rssi_value()
        print(f"data: {received_data} | 신호 강도 (RSSI): {rssi} dBm")
        self.set_mode(LoRaConstants.MODE.RXCONT)  # 계속 수신 모드로 설정

# 수신기 실행
receiver = LoRaReceiver(verbose=False)
receiver.set_mode(LoRaConstants.MODE.RXCONT)  # 수신 모드 설정

try:
    print("LoRa start...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n종료 중...")
    receiver.set_mode(LoRaConstants.MODE.SLEEP)
    BOARD.teardown()
    print("LoRa 종료 완료")
