/*
 * Platform Controller - Servo Control
 * Controls two servos based on roll/pitch commands
 *
 * Wiring:
 * - Roll Servo Signal -> Pin 9
 * - Pitch Servo Signal -> Pin 10
 * - Both Servo GND -> Arduino GND
 * - Both Servo VCC -> External 5V (recommended)
 */

#include <Servo.h>

Servo rollServo;
Servo pitchServo;

const float ROLL_CENTER = 90.0;
const float PITCH_CENTER = 90.0;
const float ANGLE_SCALE = 1.0;

void setup() {
  Serial.begin(9600);

  rollServo.attach(9);
  pitchServo.attach(10);

  rollServo.write(ROLL_CENTER);
  pitchServo.write(PITCH_CENTER);

  Serial.println("Platform Controller - Servo Mode");
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');

    command.remove(0, 1);
    command.remove(command.length() - 1);

    int commaIndex = command.indexOf(',');
    if (commaIndex > 0) {
      float roll = command.substring(0, commaIndex).toFloat();
      float pitch = command.substring(commaIndex + 1).toFloat();

      int rollServoAngle = constrain(ROLL_CENTER + (roll * ANGLE_SCALE), 0, 180);
      int pitchServoAngle = constrain(PITCH_CENTER + (pitch * ANGLE_SCALE), 0, 180);

      rollServo.write(rollServoAngle);
      pitchServo.write(pitchServoAngle);
    }
  }
}
