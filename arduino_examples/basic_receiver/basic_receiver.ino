/*
 * Basic Platform Controller Receiver
 * Receives and displays serial commands
 * Use to verify communication before connecting servos
 */

void setup() {
  Serial.begin(9600);
  Serial.println("Platform Controller - Basic Receiver");
  Serial.println("Waiting for commands...");
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');

    // Remove < and > characters
    command.remove(0, 1);  // Remove '<'
    command.remove(command.length() - 1);  // Remove '>'

    // Parse roll and pitch
    int commaIndex = command.indexOf(',');
    if (commaIndex > 0) {
      float roll = command.substring(0, commaIndex).toFloat();
      float pitch = command.substring(commaIndex + 1).toFloat();

      // Print received values
      Serial.print("Roll: ");
      Serial.print(roll);
      Serial.print(" | Pitch: ");
      Serial.println(pitch);
    }
  }
}
