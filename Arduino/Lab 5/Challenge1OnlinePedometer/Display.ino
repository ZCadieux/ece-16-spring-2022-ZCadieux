// OLED Library includes
#include "U8x8lib.h" // include the fast graphics library
#include "Wire.h"    // include the I2C library

/* 
 * Instantiate the display object "oled" and reset it using the
 * predefined argument "U8X8_PIN_NONE"
 * NOTE: if you have trouble with this constructor call, your OS
 * might require that you specify the I2C pins (22 and 23) as
 * arguments. If that is the case, you would change the call to this:
 * U8X8_SSD1306_128X32_UNIVISION_HW_I2C oled(U8X8_PIN_NONE, 22, 23);
 */
U8X8_SSD1306_128X32_UNIVISION_HW_I2C oled(U8X8_PIN_NONE);

// Clear the display no more than once per second
const int MAX_REFRESH = 1000;
unsigned long lastClear = 0;

void setupDisplay() {   
    oled.begin(); // Initializes u8x8 object
    oled.setPowerSave(0); // Makes sure OLED doesn't go to sleep
    oled.setFont(u8x8_font_amstrad_cpc_extended_r); // Set the font
    oled.setCursor(0, 0); //Sets the cursor at the top left corner
}

/*
 * A function to write a message on the OLED display.
 * The "row" argument specifies which row to print on: [0,1,2,3].
 * The "erase" argument specifies if the display should be cleared.
 */
void writeDisplay(const char * message, int row, bool erase) {
    unsigned long now = millis();
    //if erase is true and it's been longer than MAX_REFRESH (1s)
    if(erase && (millis() - lastClear >= MAX_REFRESH)) {
        oled.clearDisplay();
        lastClear = now;
    }
    oled.setCursor(0, row);
    oled.print(message);
}

/*
 * A function to write a CSV message on multiple lines on the OLED.
 * The "commaCount" argument says how many commas are in the String.
 * NOTE: The OLED can only display 4 lines (a maximum of 3 commas).
 */
void writeDisplayCSV(String message, int commaCount) {
     int startIndex = 0;
     for(int i=0; i<=commaCount; i++) {
          // find the index of the comma and store it in startIndex
          int index = message.indexOf(',', startIndex);           

          // take everything in the string up until the comma
          String subMessage = message.substring(startIndex, index); 

          startIndex = index + 1; // skip over the comma

          // Write the substring onto the OLED!
          writeDisplay(subMessage.c_str(), i, false);
     }
}
