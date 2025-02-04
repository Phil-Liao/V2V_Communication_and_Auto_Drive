// Include Libraries
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

// Create an RF24 object
RF24 radio(9, 8);  // CE, CSN

// Address through which two modules communicate.
const byte address[6] = "00001";

void start_radio(const byte address[6]) {
  radio.begin();
  // Set the address for reading
  radio.openReadingPipe(0, address);
  // Set module as receiver
  radio.startListening();
}

bool receive() {
  // Read the data if available in buffer
  if (radio.available()) {
    char text[32] = {0}; // Initialize text with null characters
    radio.read(&text, sizeof(text));
    if (strcmp(text, "true") == 0) { // Use strcmp for string comparison
      return true;
    } else {
      return false;
    }
  }
  return false; // Add a default return value in case no data is available
}

void setup() {
  while (!Serial); // Wait for serial communication to be established
  Serial.begin(9600);

  start_radio(address);
}

void loop() {
  bool condition = receive();
  Serial.println(condition);
}