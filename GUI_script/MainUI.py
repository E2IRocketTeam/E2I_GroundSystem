import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout
from PyQt5 import uic
import serial
import pyqtgraph as pg
from PyQt5.QtGui import QFont
# uic.loadUiType returns two values, so unpack them as a tuple
form_class, base_class = uic.loadUiType("D:\\EEI\\E2I_GroundSystem\\RPI_GUI\\MainUI.ui")

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Initialize the serial port with correct port and baud rate
        #self.serial_port = serial.Serial('COM7', 115200)  # Update with the correct port

        # BNO 그래프 추가
        self.BNOgraph()

    def ResetStart(self):
        self.textEdit.append("RESET")
        ResetCode = "RESET"
        
        # Check if the serial port is open and send the reset code
        if self.serial_port.is_open:
            self.serial_port.write(ResetCode.encode())
            print(f"Sent message: {ResetCode}")
        else:
            print("Serial port is not open")

    def BNOgraph(self):
        self.BNOplot_pg = pg.PlotWidget()
        self.BNOplot_pg.setBackground('w')
           # 폰트 스타일 설정 (크기 14pt, 굵게)
        font = QFont("Arial", 12, QFont.Bold)  # 여기서 크기와 굵기 조정 가능

        # X축과 Y축 숫자 스타일 적용
        self.BNOplot_pg.getAxis("bottom").setStyle(tickFont=font)  # X축
        self.BNOplot_pg.getAxis("left").setStyle(tickFont=font)    # Y축

        # 축 설정
        self.BNOplot_pg.getAxis("bottom").setPen(pg.mkPen("black", width=2))  # X축
        self.BNOplot_pg.getAxis("left").setPen(pg.mkPen("black", width=2))    # Y축

        layout = QVBoxLayout(self.BNOplot)  # PyQt Designer에서 만든 QWidget 사용
        layout.addWidget(self.BNOplot_pg)
        self.BNOplot.setLayout(layout)  # 레이아웃 적용

# Create QApplication instance
app = QApplication(sys.argv)

# Show the main window
main_window = WindowClass()
main_window.show()

# Run the application event loop
sys.exit(app.exec_())
