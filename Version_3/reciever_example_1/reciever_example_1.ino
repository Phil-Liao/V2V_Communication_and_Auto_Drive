#include <SPI.h>      //啟用SCK,MOSI,MISO引腳
#include "nRF24L01.h" //啟用nRF24L01h參數
#include "RF24.h"
int Vx, Vy;
int LED_B = 2;     // LED引腳
int LED_R = 3;     // LED引腳
int LED_G = 4;     // LED引腳
int joystick[3];   // 三個讀取陣列
RF24 radio(9, 10); // CE,CSN通訊引腳
// 讀取和寫入的代號
const uint64_t pipes[2] = {0xF7F0F0F0E1LL, 0xF7F0F0F0D2LL};
void setup(void)
{
    pinMode(LED_B, OUTPUT);             // 設LED引腳為輸出
    pinMode(LED_R, OUTPUT);             // 設LED引腳為輸出
    pinMode(LED_G, OUTPUT);             // 設LED引腳為輸出
    Serial.begin(57600);                // 啟用57600鮑率
    radio.begin();                      // 啟用nRF24L01
    radio.setRetries(15, 15);           // 重試次數
    radio.openReadingPipe(1, pipes[1]); // 開啟讀取通道
    radio.startListening();             // 開始傾聽資訊
    radio.printDetails();               // 寫出無線電狀態
    radio.openWritingPipe(pipes[1]);    // 開啟寫入通道
    radio.openReadingPipe(1, pipes[0]); // 開啟讀取通道
    radio.startListening();             // 開始傾聽資訊
}
void loop()
{
    if (radio.available())
    {                                           // 如果有Radio訊號
        radio.read(joystick, sizeof(joystick)); // 透過無線電讀取joystick陣列
        Vx = joystick[0] * 0.175;
        Vy = joystick[1] * 0.175;
        if (Vx > 80 && Vx < 100 && Vy > 80 && Vy < 100)
        {
            Serial.println("OFF");
            digitalWrite(LED_B, LOW);
            digitalWrite(LED_R, LOW);
            digitalWrite(LED_G, LOW);
            delay(150);
        }
        if (Vx > 113 && Vy > 67 && Vy < 113)
        {
            Serial.println("B_OB");
            digitalWrite(LED_B, HIGH);
            digitalWrite(LED_R, LOW);
            digitalWrite(LED_G, LOW);
            delay(150);
        }
        if (Vx < 67 && Vy > 67 && Vy < 113)
        {
            Serial.println("R_ON");
            digitalWrite(LED_B, LOW);
            digitalWrite(LED_R, HIGH);
            digitalWrite(LED_G, LOW);
            delay(150);
        }
        if (Vy < 67 && Vx > 67 && Vx < 113)
        {
            Serial.println("G_ON");
            digitalWrite(LED_B, LOW);
            digitalWrite(LED_R, LOW);
            digitalWrite(LED_G, HIGH);
            delay(150);
        }
        if (Vy > 113 && Vx > 67 && Vx < 113)
        {
            Serial.println("All_ON");
            digitalWrite(LED_B, HIGH);
            digitalWrite(LED_R, HIGH);
            digitalWrite(LED_G, HIGH);
            delay(150);
        }
        if (joystick[2] == 1)
        {
            digitalWrite(LED_B, HIGH);
            digitalWrite(LED_R, LOW);
            digitalWrite(LED_G, LOW);
            delay(1000);
            digitalWrite(LED_B, LOW);
            digitalWrite(LED_R, HIGH);
            digitalWrite(LED_G, LOW);
            digitalWrite(LED_B, LOW);
            delay(1000);
            digitalWrite(LED_B, LOW);
            digitalWrite(LED_R, LOW);
            digitalWrite(LED_G, HIGH);
            delay(1000);
        }
        delay(20);
    }
}