#include <stdio.h>
#include <stdint.h>
#include <wiringPi.h>
#include <wiringPiSPI.h>

#define SPI_CHANNEL 0  // SPI Channel (CE0)
#define SPI_SPEED 500000  // SPI Speed

#define CS_PIN 5    // Chip Select (NSS) - GPIO5 (Pin 29)
#define RESET_PIN 25 // Reset - GPIO25 (Pin 22)
#define DIO0_PIN 4   // DIO0 Interrupt - GPIO4 (Pin 7)

// LoRa Register Addresses
#define REG_VERSION 0x42
#define REG_FRF_MSB 0x06
#define REG_FRF_MID 0x07
#define REG_FRF_LSB 0x08
#define REG_IRQ_FLAGS 0x12

// 915 MHz Frequency Settings (Default: 0xE4C000)
#define FREQ_915_MHZ_MSB 0xE4
#define FREQ_915_MHZ_MID 0xC0
#define FREQ_915_MHZ_LSB 0x00

void rfm95w_write_register(uint8_t reg, uint8_t value) {
    uint8_t data[2] = { reg | 0x80, value }; // Write mode (MSB 1)
    digitalWrite(CS_PIN, LOW);
    wiringPiSPIDataRW(SPI_CHANNEL, data, 2);
    digitalWrite(CS_PIN, HIGH);
}

uint8_t rfm95w_read_register(uint8_t reg) {
    uint8_t data[2] = { reg & 0x7F, 0x00 }; // Read mode (MSB 0)
    digitalWrite(CS_PIN, LOW);
    wiringPiSPIDataRW(SPI_CHANNEL, data, 2);
    digitalWrite(CS_PIN, HIGH);
    return data[1];
}

void rfm95w_reset() {
    digitalWrite(RESET_PIN, LOW);
    delay(10);
    digitalWrite(RESET_PIN, HIGH);
    delay(10);
}

void rfm95w_init() {
    // Reset the module
    rfm95w_reset();
    delay(100);

    // Read Version Register (should return 0x12)
    uint8_t version = rfm95w_read_register(REG_VERSION);
    if (version == 0x12) {
        printf("✅ LoRa Module detected: SX1276 (RFM95W) Version: 0x%X\n", version);
    } else {
        printf("❌ Error: LoRa Module not detected! (Version: 0x%X)\n", version);
        return;
    }

    // Set Frequency to 915MHz
    rfm95w_write_register(REG_FRF_MSB, FREQ_915_MHZ_MSB);
    rfm95w_write_register(REG_FRF_MID, FREQ_915_MHZ_MID);
    rfm95w_write_register(REG_FRF_LSB, FREQ_915_MHZ_LSB);

    // Verify Frequency Setting
    uint8_t frf_msb = rfm95w_read_register(REG_FRF_MSB);
    uint8_t frf_mid = rfm95w_read_register(REG_FRF_MID);
    uint8_t frf_lsb = rfm95w_read_register(REG_FRF_LSB);
    printf("📡 LoRa Frequency Set: %02X %02X %02X (Expected: E4 C0 00)\n", frf_msb, frf_mid, frf_lsb);
}

int main() {
    if (wiringPiSetup() == -1) {
        printf("❌ wiringPi Initialization Failed!\n");
        return -1;
    }

    pinMode(CS_PIN, OUTPUT);
    pinMode(RESET_PIN, OUTPUT);
    pinMode(DIO0_PIN, INPUT);
    digitalWrite(CS_PIN, HIGH);
    digitalWrite(RESET_PIN, HIGH);

    if (wiringPiSPISetup(SPI_CHANNEL, SPI_SPEED) == -1) {
        printf("❌ SPI Initialization Failed!\n");
        return -1;
    }

    printf("🔄 Initializing LoRa Module...\n");
    rfm95w_init();

    printf("🎯 Waiting for LoRa Messages...\n");

    while (1) {
        uint8_t irqFlags = rfm95w_read_register(REG_IRQ_FLAGS);
        if (irqFlags & 0x40) { // RxDone flag
            printf("📩 LoRa Packet Received!\n");
            rfm95w_write_register(REG_IRQ_FLAGS, 0xFF);
        }
        delay(100);
    }

    return 0;
}
