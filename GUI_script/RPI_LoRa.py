import spidev
import RPi.GPIO as GPIO
import time

# Pin configuration
PIN_RST = 25  # LoRa RESET pin
PIN_CS = 5    # LoRa SPI Chip Select (NSS)
PIN_DIO0 = 4  # LoRa IRQ (Interrupt Request)

# Register addresses
REG_FIFO = 0x00
REG_OP_MODE = 0x01
REG_FRF_MSB = 0x06
REG_FRF_MID = 0x07
REG_FRF_LSB = 0x08
REG_VERSION = 0x42
MODE_SLEEP = 0x00
MODE_RX_CONTINUOUS = 0x85
MODE_LONG_RANGE_MODE = 0x80

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Device 0 (CE0)
spi.max_speed_hz = 5000000

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_RST, GPIO.OUT)
GPIO.setup(PIN_CS, GPIO.OUT)
GPIO.setup(PIN_DIO0, GPIO.IN)

def reset_lora():
    """ Reset the LoRa module """
    GPIO.output(PIN_RST, GPIO.LOW)
    time.sleep(0.01)
    GPIO.output(PIN_RST, GPIO.HIGH)
    time.sleep(0.01)

def spi_write(reg, value):
    """ SPI write function """
    GPIO.output(PIN_CS, GPIO.LOW)
    spi.xfer2([reg | 0x80, value])
    GPIO.output(PIN_CS, GPIO.HIGH)

def spi_read(reg):
    """ SPI read function """
    GPIO.output(PIN_CS, GPIO.LOW)
    resp = spi.xfer2([reg & 0x7F, 0])
    GPIO.output(PIN_CS, GPIO.HIGH)
    return resp[1]

def set_frequency():
    """ Set the frequency to 915MHz """
    spi_write(REG_FRF_MSB, 0xE4)
    spi_write(REG_FRF_MID, 0xC0)
    spi_write(REG_FRF_LSB, 0x00)
    print("Frequency set to 915MHz!")

def init_lora():
    """ Initialize the LoRa module """
    reset_lora()
    version = spi_read(REG_VERSION)
    if version != 0x12:
        print("LoRa module not detected!")
        return False

    # Switch to sleep mode
    spi_write(REG_OP_MODE, MODE_SLEEP)
    time.sleep(0.1)

    # Set LoRa mode
    spi_write(REG_OP_MODE, MODE_LONG_RANGE_MODE)

    # Set frequency to 915MHz
    set_frequency()

    print("LoRa module initialized! (915MHz, Receiver mode)")
    return True

def parse_sensor_data(data):
    """ Parse CSV-formatted sensor data """
    try:
        values = data.split(",")
        sensor_data = {
            "yaw": float(values[0]),
            "pitch": float(values[1]),
            "roll": float(values[2]),
            "temperature": float(values[3]),
            "pressure": float(values[4]),
            "altitude": float(values[5])
        }
        return sensor_data
    except (IndexError, ValueError):
        print("Invalid data format received!")
        return None

def receive_lora_message():
    """ Receive a LoRa message and display sensor data in CLI """
    spi_write(REG_OP_MODE, MODE_RX_CONTINUOUS)
    print("📡 Waiting for incoming sensor data...\n")

    while True:
        if GPIO.input(PIN_DIO0) == 1:
            length = spi_read(REG_FIFO)  # Read received data length
            message = "".join(chr(spi_read(REG_FIFO)) for _ in range(length))
            
            # Check for RESET command
            if message.strip() == "RESET":
                print("\nReceived RESET command. Rebooting system...\n")
                reset_lora()
                return

            # Parse and display sensor data
            sensor_data = parse_sensor_data(message)
            if sensor_data:
                print("="*50)
                print(f"Yaw: {sensor_data['yaw']}°")
                print(f"Pitch: {sensor_data['pitch']}°")
                print(f"Roll: {sensor_data['roll']}°")
                print(f"Temperature: {sensor_data['temperature']}°C")
                print(f"Pressure: {sensor_data['pressure']} hPa")
                print(f"Altitude: {sensor_data['altitude']} m")
                print("="*50 + "\n")

# Main execution
if __name__ == "__main__":
    if init_lora():
        while True:
            receive_lora_message()
