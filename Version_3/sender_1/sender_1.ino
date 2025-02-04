//Include Libraries
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

//create an RF24 object
RF24 radio(9, 8);  // CE, CSN

//address through which two modules communicate.
const byte address[6] = "00001";

void start_radio(const byte address[6]) {
  radio.begin();
  //set the address
  radio.openWritingPipe(address);
  //Set module as transmitter
  radio.stopListening();
}

void send_message(bool condition) {
  char text[6]; // Declare text outside the if/else blocks
  if (condition == true) {
    strcpy(text, "true");
  } else {
    strcpy(text, "false");
  }
  radio.write(&text, sizeof(text));
  delay(1000);
}

void setup() {
  start_radio(address);
}

void loop() {
  send_message(true);
}