#include <SPI.h>
#include <MFRC522.h>

/*
 * Install needed libraries and flash to arduino
 * Connect RC522 to Arduino using the following pin layout
 * 
 * Pin layout used:
 * -----------------------------------
 *             MFRC522      Arduino   
 *             Reader/PCD   Mega      
 * Signal      Pin          Pin       
 * -----------------------------------         
 * SPI SS      SDA(SS)      53
 * SPI SCK     SCK          52        
 * SPI MOSI    MOSI         51        
 * SPI MISO    MISO         50
 * IRQ         IRQ          unconnected
 * GND         GND          GND                
 * RST/Reset   RST          2
 * 3.3V        3.3V         3.3V
 * 	
 */

#define RST_PIN 2
#define SS_PIN 53

MFRC522 mfrc522(SS_PIN, RST_PIN);

//Setup the serial port and RFID reader
void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  // Determines encoded hex UID of RFID chip 
  String content = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  
  // Send UID to Python script over serial port
  Serial.println(content);
  
  delay(1000); // Optional delay to avoid repeated readings
}
