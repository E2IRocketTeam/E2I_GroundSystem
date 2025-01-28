import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import serial
from BNO055_Visualizer import BNO055Visualizer
from threading import Thread

form_class, base_class = uic.loadUiType("D:\EEI\E2I_GroundSystem\RPI_GUI\MainUI.ui")

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.textEdit.append("Program Initialized")

        # 시리얼 포트 초기화
        self.serial_port = serial.Serial('COM7', 9600, timeout=0.005)
        self.serial_port.flush()

        # Visualizer 초기화
        self.visualizer = BNO055Visualizer(self.serial_port)
        self.running = False

        # 버튼 이벤트 연결
        self.resetButton.clicked.connect(self.ResetStart)
        self.startButton.clicked.connect(self.start_visualization)

    def ResetStart(self):
        self.textEdit.append("RESET")
        ResetCode = "RESET"
        if self.serial_port.is_open:
            self.serial_port.write(ResetCode.encode())
            print(f"Sent message: {ResetCode}")
        else:
            print("Serial port is not open")

    def start_visualization(self):
        if not self.running:
            self.running = True
            self.textEdit.append("Starting Visualization...")
            self.thread = Thread(target=self.visualizer.start)
            self.thread.start()

# PyQt Application 시작
app = QApplication(sys.argv)
main_window = WindowClass()
main_window.show()
sys.exit(app.exec_())
