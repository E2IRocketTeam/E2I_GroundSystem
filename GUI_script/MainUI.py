import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import serial
from BNOGraph import BNOGraph  # 2D 그래프 클래스
from BNO3DGraph import BNO3DGraph  # 3D 그래프 클래스

# UI 로드
form_class, base_class = uic.loadUiType("D:\\EEI\\E2I_GroundSystem\\RPI_GUI\\MainUI.ui")

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.serial_port = serial.Serial('COM3', 115200, timeout=0.005)

        # 2D 그래프 초기화
        self.bno_graph = BNOGraph(self.BNOplot, self.serial_port)

        # 3D 그래프 초기화 (BNO3D 위젯 사용)
        self.bno_3d_graph = BNO3DGraph(self.BNO3D)  # widget_2 대신 BNO3D 사용

    def ResetStart(self):
        self.textEdit.append("RESET")
        ResetCode = "RESET"
        
        # 시리얼 포트가 열려 있으면 리셋 코드 전송
        if self.serial_port.is_open:
            self.serial_port.write(ResetCode.encode())
            print(f"Sent message: {ResetCode}")
        else:
            print("Serial port is not open")

# 실행
app = QApplication(sys.argv)
main_window = WindowClass()
main_window.show()
sys.exit(app.exec_())