void setup() {
    setupDisplay();
}
void loop() {
    writeDisplay("Display on Row 0", 0, true);
    delay(1000);
    writeDisplay("Display on Row 1", 1, false);
    delay(1000);
    writeDisplay("Display on Row 2", 2, false);
    delay(1000);
    writeDisplay("Cleared Display", 0, true);
    delay(1000);
}
