import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from PyQt5.QtCore import QTimer
import serial

# uic.loadUiType returns two values, so unpack them as a tuple
form_class, base_class = uic.loadUiType("/home/E2I/E2I_WorkSpace/Avionics_RPI/RPI_GUI/MainUI.ui")

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Initialize the serial port with correct port and baud rate
        try:
            self.serial_port = serial.Serial('/dev/ttyACM0', 9600)  # Update with the correct port
        except serial.SerialException as e:
            print(f"Failed to connect to serial port: {e}")
            self.serial_port = None

        # Set up a QTimer to read from serial port periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_serial)
        self.timer.start(1000)  # 1 second interval

    def read_serial(self):
        # Check if the serial port is available and open
        if self.serial_port and self.serial_port.is_open:
            # Read a line from the serial port
            if self.serial_port.in_waiting > 0:
                data = self.serial_port.readline().decode().strip()
                # Display data in the textEdit widget and print it
                self.textEdit.append(f"Arduino: {data}")
                print(f"Arduino: {data}")
        else:
            print("Serial port is not available or not open")

# Create QApplication instance
app = QApplication(sys.argv)

# Show the main window
main_window = WindowClass()
main_window.show()

# Run the application event loop
sys.exit(app.exec_())
