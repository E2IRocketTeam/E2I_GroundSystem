import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout
from PyQt5 import uic
import serial
import pyqtgraph as pg

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
        self.plotWidget_pg = pg.PlotWidget()
        self.plotWidget_pg.setBackground('w')
        layout = QVBoxLayout(self.plotWidget)  # PyQt Designer에서 만든 QWidget 사용
        layout.addWidget(self.plotWidget_pg)
        self.plotWidget.setLayout(layout)  # 레이아웃 적용

# Create QApplication instance
app = QApplication(sys.argv)

# Show the main window
main_window = WindowClass()
main_window.show()

# Run the application event loop
sys.exit(app.exec_())
