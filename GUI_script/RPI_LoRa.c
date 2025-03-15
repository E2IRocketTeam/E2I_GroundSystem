#include <stdio.h>
#include <stdint.h>
#include <wiringPi.h>
#include <wiringPiSPI.h>

#define SPI_CHANNEL 0
#define SPI_SPEED 500000
#define CS_PIN 5
#define RESET_PIN 25

#define REG_IRQ_FLAGS 0x12
#define REG_FIFO 0x00
#define REG_RX_NB_BYTES 0x13
#define REG_FIFO_RX_CURRENT_ADDR 0x10

void rfm95w_write_register(uint8_t reg, uint8_t value) {
    uint8_t data[2] = { reg | 0x80, value };
    digitalWrite(CS_PIN, LOW);
    wiringPiSPIDataRW(SPI_CHANNEL, data, 2);
    digitalWrite(CS_PIN, HIGH);
}

uint8_t rfm95w_read_register(uint8_t reg) {
    uint8_t data[2] = { reg & 0x7F, 0x00 };
    digitalWrite(CS_PIN, LOW);
    wiringPiSPIDataRW(SPI_CHANNEL, data, 2);
    digitalWrite(CS_PIN, HIGH);
    return data[1];
}

int main() {
    wiringPiSetup();
    pinMode(CS_PIN, OUTPUT);
    pinMode(RESET_PIN, OUTPUT);
    digitalWrite(CS_PIN, HIGH);
    digitalWrite(RESET_PIN, HIGH);
    wiringPiSPISetup(SPI_CHANNEL, SPI_SPEED);

    printf("Raspberry Pi 4: LoRa Receiver Ready (915MHz)\n");

    while (1) {
        uint8_t irqFlags = rfm95w_read_register(REG_IRQ_FLAGS);
        if (irqFlags & 0x40) {
            printf("Packet Received!\n");

            uint8_t len = rfm95w_read_register(REG_RX_NB_BYTES);
            uint8_t buf[255] = {0};
            for (uint8_t i = 0; i < len; i++) {
                buf[i] = rfm95w_read_register(REG_FIFO);
            }

            printf("Received Data: ");
            for (uint8_t i = 0; i < len; i++) {
                printf("%c", buf[i]);
            }
            printf("\n");

            rfm95w_write_register(REG_IRQ_FLAGS, 0xFF);
        }
        delay(100);
    }

    return 0;
}
