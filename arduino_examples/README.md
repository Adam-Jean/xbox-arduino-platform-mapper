# Arduino Examples

This directory contains Arduino sketches for receiving and using data from the Platform Controller application.

## Serial Communication Protocol

The Platform Controller sends data in this format:
```
<roll,pitch>\n
```

**Example:** `<12.5,-8.3>\n`

**Details:**
- **Baudrate:** 9600
- **Format:** Angle-bracket delimited, comma-separated floats
- **Rate:** 20 commands per second
- **Roll Range:** -45.0 to +45.0 degrees
- **Pitch Range:** -45.0 to +45.0 degrees

## Sketches

### 1. Basic Receiver (`basic_receiver/`)

**Purpose:** Test serial communication before connecting hardware

**Use this to:**
- Verify the serial connection works
- Debug port issues
- Check data format
- Confirm baudrate settings

**How to use:**
1. Upload `basic_receiver.ino` to your Arduino
2. Open Serial Monitor (9600 baud)
3. Start Platform Controller and connect to the Arduino's port
4. You should see: `Roll: 12.5 | Pitch: -8.3` updating in real-time

### 2. Servo Control (`servo_control/`)

**Purpose:** Complete working example with servo motors

**Hardware Required:**
- Arduino Uno or Nano
- 2x Servo motors (SG90 or similar)
- External 5V power supply (recommended for servos)
- Jumper wires

**Wiring Diagram:**

```
Roll Servo:
  Signal (Orange/Yellow) -> Arduino Pin 9
  Power (Red)            -> 5V (external supply recommended)
  Ground (Brown/Black)   -> Arduino GND

Pitch Servo:
  Signal (Orange/Yellow) -> Arduino Pin 10
  Power (Red)            -> 5V (external supply)
  Ground (Brown/Black)   -> Arduino GND

IMPORTANT: Connect external 5V supply ground to Arduino GND
```

**Pin Configuration:**
- Pin 9: Roll servo control
- Pin 10: Pitch servo control

**How to use:**
1. Wire servos as shown above
2. Upload `servo_control.ino` to Arduino
3. Start Platform Controller
4. Connect to Arduino's serial port
5. Move Xbox controller - servos should respond

## Calibration

### Center Position
Default center position is 90 degrees for both servos. If your platform is tilted at rest:

**In `servo_control.ino`, adjust:**
```cpp
const float ROLL_CENTER = 90.0;   // Change to 85-95 if tilted
const float PITCH_CENTER = 90.0;  // Change to 85-95 if tilted
```

### Sensitivity
If servos move too much or too little:

**Adjust the scale factor:**
```cpp
const float ANGLE_SCALE = 1.0;  // Decrease to 0.5 for less movement
                                 // Increase to 2.0 for more movement
```

### Reverse Direction
If a servo moves backward:

**Change the sign in the calculation:**
```cpp
// Original:
int rollServoAngle = constrain(ROLL_CENTER + (roll * ANGLE_SCALE), 0, 180);

// Reversed:
int rollServoAngle = constrain(ROLL_CENTER - (roll * ANGLE_SCALE), 0, 180);
```

## Troubleshooting

### No Serial Data
- Check baudrate matches (9600)
- Verify Arduino is selected in Platform Controller
- Try unplugging/replugging USB cable
- Close Arduino IDE Serial Monitor (port conflict)

### Servos Jittering
- **Power issue:** Use external 5V supply for servos
- **Noise:** Add 100µF capacitor across servo power pins
- **Signal:** Keep servo wires under 12 inches

### Servos Not Moving
- Check wiring (signal to correct pin)
- Verify servo power connection
- Test servo with Arduino Sweep example first
- Ensure Platform Controller is in "Serial" mode, not "Test Mode"

### Platform Drifting
- Increase deadzone in Platform Controller settings
- Calibrate center positions in Arduino code
- Check controller thumbsticks for wear

## Extending the Code

### Adding More Servos
```cpp
Servo yawServo;  // Add third servo

void setup() {
  yawServo.attach(11);  // Use pin 11
  yawServo.write(90);
}
```

### Using Different Actuators
Replace `Servo.h` library with:
- **Stepper motors:** `Stepper.h`
- **DC motors:** H-bridge (L298N) with PWM
- **LEDs:** `analogWrite()` for brightness control

### Adding Smoothing
```cpp
// Exponential smoothing
float smoothedRoll = 0;
const float alpha = 0.2;  // Smoothing factor (0-1)

smoothedRoll = (alpha * roll) + ((1 - alpha) * smoothedRoll);
```

## Platform-Specific Port Names

**Windows:**
- `COM3`, `COM4`, `COM5`, etc.
- Check Device Manager -> Ports (COM & LPT)

**Mac:**
- `/dev/cu.usbserial-*`
- `/dev/cu.usbmodem-*`
- Use `cu` not `tty` for Arduino

**Linux:**
- `/dev/ttyUSB0`, `/dev/ttyUSB1` (FTDI, CH340)
- `/dev/ttyACM0`, `/dev/ttyACM1` (native USB)
- May need: `sudo usermod -a -G dialout $USER`

## Additional Resources

**Driver Downloads:**
- CH340 (Arduino clones): https://sparks.gogo.co.nz/ch340.html
- FTDI: https://ftdichip.com/drivers/vcp-drivers/
- CP2102: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers

**Arduino Libraries:**
- Servo: Built-in (no installation needed)
- For advanced servo control: `ServoEasing` library

**Testing Tools:**
- Arduino Serial Monitor (Tools -> Serial Monitor)
- PuTTY (Windows)
- screen (Mac/Linux): `screen /dev/ttyUSB0 9600`
