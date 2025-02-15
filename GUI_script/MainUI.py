import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import serial
from BNOGraph import BNOGraph  # 새로 만든 파일에서 클래스 가져오기

# UI 로드
form_class, base_class = uic.loadUiType("D:\\EEI\\E2I_GroundSystem\\RPI_GUI\\MainUI.ui")

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.serial_port = serial.Serial('COM3', 115200, timeout=0.005)
        self.bno_graph = BNOGraph(self.BNOplot, self.serial_port)

    def ResetStart(self):
        self.textEdit.append("RESET")
        ResetCode = "RESET"
        
        # Check if the serial port is open and send the reset code
        if self.serial_port.is_open:
            self.serial_port.write(ResetCode.encode())
            print(f"Sent message: {ResetCode}")
        else:
            print("Serial port is not open")
        # 시리얼 포트 설정 (COM 포트 확인 필요)
        

# 실행
app = QApplication(sys.argv)
main_window = WindowClass()
main_window.show()
sys.exit(app.exec_())
