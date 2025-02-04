#include <SPI.h>      //啟用SCK,MOSI,MISO引腳
#include "nRF24L01.h" //啟用nRF24L01h參數
#include "RF24.h"
#include <ezButton.h> //啟用SW按鍵參數
ezButton button(2);   // SW接第二引腳
int VRX_Pin = A0;     // VRX引腳
int VRY_Pin = A1;     // VRY引腳
int SW;               // SW引腳的預設讀值
int joystick[3];      // 三個引腳讀值的儲存陣列
RF24 radio(9, 10);    // CE,CSN通訊引腳
// 讀取和寫入的代號
const uint64_t pipes[2] = {0xF7F0F0F0E1LL, 0xF7F0F0F0D2LL};
void setup() {
    Serial.begin(57600);                // 啟用57600鮑率
    radio.begin();                      // 啟用nRF24L01
    radio.setRetries(15, 15);           // 重試次數
    radio.openReadingPipe(1, pipes[1]); // 開啟讀取通道
    radio.startListening();             // 開始傾聽資訊
    radio.printDetails();               // 印出radio的情況
    radio.openWritingPipe(pipes[0]);    // 開啟寫入通道
    radio.openReadingPipe(1, pipes[1]); // 開啟讀取通道
    radio.stopListening();              // 停止傾聽資訊
}
void loop(void) {
    radio.stopListening();  // 停止傾聽資訊
    button.loop();          // 啟用button迴圈
    if (button.isPressed()) // 當按鈕按下
        SW = 1;
    if (button.isReleased()) // 當按鈕釋放
        SW = 0;
    joystick[0] = analogRead(VRX_Pin);       // 將類比訊號的讀值寫路陣列[0]
    joystick[1] = analogRead(VRY_Pin);       // 將類比訊號的讀值寫路陣列[1]
    joystick[2] = SW;                        ////SW讀值寫路陣列[3]
    Serial.print(joystick[0]);               // 印出joystick[0]讀值
    Serial.print(",");                       // 印出",""
    Serial.print(joystick[1]);               // 印出joystick[1]讀值
    Serial.print(",");                       // 印出",""
    Serial.print(joystick[2]);               // 印出joystick[2]讀值
    Serial.print("\n");                      // 換行
    radio.write(joystick, sizeof(joystick)); // 透過無線電傳送joystick陣列
    radio.startListening();                  // 重啟無線電陣列
    delay(100);                              // 等待0.1秒
}
