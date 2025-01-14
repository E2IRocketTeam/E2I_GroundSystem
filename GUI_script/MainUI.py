import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import serial

# uic.loadUiType returns two values, so unpack them as a tuple
form_class, base_class = uic.loadUiType("/home/E2I/E2I_WorkSpace/Avionics_RPI/RPI_GUI/MainUI.ui")

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Initialize the serial port with correct port and baud rate
        self.serial_port = serial.Serial('/dev/ttyACM0', 9600)  # Update with the correct port

    def ResetStart(self):
        self.textEdit.append("RESET")
        ResetCode = "RESET"
        # Check if the serial port is open and send the reset code
        if self.serial_port.is_open:
            self.serial_port.write(ResetCode.encode())
            print(f"Sent message: {ResetCode}")
        else:
            print("Serial port is not open")

# Create QApplication instance
app = QApplication(sys.argv)

# Show the main window
main_window = WindowClass()
main_window.show()

# Run the application event loop
sys.exit(app.exec_())


