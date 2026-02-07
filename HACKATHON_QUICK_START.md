# Hackathon Quick Start Guide

**Goal:** Get Platform Controller running in under 5 minutes.

## Prerequisites Checklist

- [ ] Python 3.7+ installed
- [ ] Xbox controller (USB or Bluetooth)
- [ ] Arduino with USB cable (optional - works without for testing)

## 5-Minute Setup

### Windows

```cmd
# 1. Clone or download project
git clone https://github.com/Adam-Jean/xbox-arduino-platform-mapper.git
cd xbox-arduino-platform-mapper

# 2. Run (creates venv automatically)
run.bat
```

### Mac

```bash
# 1. Clone or download project
git clone https://github.com/Adam-Jean/xbox-arduino-platform-mapper.git
cd xbox-arduino-platform-mapper

# 2. Make script executable
chmod +x run.sh

# 3. Run (creates venv automatically)
./run.sh
```

### Linux

```bash
# 1. Clone or download project
git clone https://github.com/Adam-Jean/xbox-arduino-platform-mapper.git
cd xbox-arduino-platform-mapper

# 2. Add user to dialout group (needed for serial access)
sudo usermod -a -G dialout $USER
# Log out and log back in, then:

# 3. Make script executable
chmod +x run.sh

# 4. Run (creates venv automatically)
./run.sh
```

## Test Without Hardware (30 seconds)

**No Arduino? No problem!**

1. Launch the application (using steps above)
2. Check "Test Mode" checkbox
3. Connect your Xbox controller (plug in USB or pair Bluetooth)
4. Move the joysticks - watch the 3D platform tilt

**This confirms:**
- ✅ Python environment works
- ✅ Controller is detected
- ✅ Application runs correctly

## Connect Arduino (3 steps)

### Step 1: Upload Arduino Sketch

1. Open Arduino IDE
2. File -> Open -> `arduino_examples/basic_receiver/basic_receiver.ino`
3. Select your board: Tools -> Board -> Arduino Uno (or your model)
4. Select port: Tools -> Port -> COM3 (Windows) or /dev/cu.usbserial (Mac)
5. Click Upload (→)

### Step 2: Close Serial Monitor

**CRITICAL:** Serial Monitor locks the port!

- Tools -> Serial Monitor -> Close it
- Only one program can use the serial port at a time

### Step 3: Connect in Platform Controller

1. Uncheck "Test Mode"
2. Click "Refresh" button next to port dropdown
3. Select your Arduino's port:
   - **Windows:** COM3, COM4, etc.
   - **Mac:** /dev/cu.usbserial-*
   - **Linux:** /dev/ttyUSB0 or /dev/ttyACM0
4. Click "Connect"

**Status should show:** "Connected to [PORT]"

## Control Modes

**Velocity Mode (default):**
- Joystick acts like a steering wheel
- Platform tilts in direction you push
- Returns to center when released
- Best for: Balancing balls, stabilization

**Position Mode:**
- Joystick position = platform angle
- Platform stays tilted when you release
- Best for: Precise positioning, manual control

**Change mode:** Settings -> Control Mode -> Select mode

## Common Issues (90% of problems)

### 1. "No controller detected"

**Fix:**
- Windows: Install Xbox driver (usually automatic)
- Linux: Install `xboxdrv` or use built-in `xpad` driver
- Test: Press buttons - LED should light up on controller
- Try different USB port

### 2. "Access denied" / "Permission denied" (Linux)

**Fix:**
```bash
# Temporary (until reboot):
sudo chmod 666 /dev/ttyUSB0

# Permanent (must log out/in after):
sudo usermod -a -G dialout $USER
```

### 3. No ports in dropdown

**Fix:**
- Unplug Arduino, plug back in
- Click "Refresh" button
- Try different USB cable (many are power-only!)
- Install CH340 driver (Arduino clones): https://sparks.gogo.co.nz/ch340.html

### 4. Platform drifts without touching controller

**Fix:**
- Settings -> Deadzone -> Increase to 0.15-0.20
- Your controller's joysticks may be worn

### 5. "Port in use" error

**Fix:**
- Close Arduino IDE Serial Monitor
- Close other serial programs (PuTTY, screen, etc.)
- Unplug Arduino for 3 seconds, plug back in

## Hardware Checklist

**Essential:**
- [ ] Xbox controller + USB cable (or Bluetooth adapter)
- [ ] Arduino Uno/Nano + USB cable
- [ ] 3+ spare USB cables (many are charge-only!)

**For Servo Control:**
- [ ] 2x SG90 servo motors (or similar)
- [ ] External 5V power supply (wall adapter or battery pack)
- [ ] Breadboard + jumper wires
- [ ] Platform mount (3D printed or cardboard)

**Drivers (download before hackathon):**
- [ ] CH340 driver (for Arduino clones)
- [ ] FTDI driver (if using FTDI boards)

## Quick Testing Workflow

```
1. Test Mode ✓ -> Verify controller works
2. Upload basic_receiver.ino -> Verify serial works
3. Upload servo_control.ino -> Verify servos work
4. Build platform -> Integrate hardware
5. Calibrate -> Adjust deadzones, response curves
```

## Response Curves (Advanced)

**Try these for different feel:**

- **Linear:** Direct 1:1 mapping (default)
- **Quadratic:** Gentle near center, aggressive at edges
- **Cubic:** Very gentle near center, very aggressive at edges
- **S-Curve:** Smooth acceleration, best for beginners
- **Exponential:** Extreme sensitivity at edges

**Change:** Settings -> Response Curve -> Select curve

## Serial Protocol (For Custom Arduino Code)

**Format:** `<roll,pitch>\n`

**Example:** `<12.5,-8.3>\n`

**Details:**
- Baudrate: 9600
- Roll/Pitch: -45.0 to +45.0 degrees
- Update rate: 20 Hz (50ms interval)

## File Locations

- Arduino examples: `arduino_examples/`
- Full documentation: `README.md`
- Configuration guide: `CONFIGURATION.md`
- Architecture details: `ARCHITECTURE.md`

## Emergency Contacts

**Issues?**
- GitHub Issues: https://github.com/Adam-Jean/xbox-arduino-platform-mapper/issues
- Documentation: See README.md

## Time-Saving Tips

1. **Test software first** - Use Test Mode to verify before touching Arduino
2. **Download drivers early** - WiFi at hackathons is unreliable
3. **Bring spare cables** - USB cable failure is #1 hardware issue
4. **Use basic_receiver.ino first** - Isolate serial issues from hardware issues
5. **Screenshot working port names** - Windows COM ports change randomly

## Success Checklist

- [ ] Application launches
- [ ] Test Mode works with controller
- [ ] Arduino receives serial data (verify in Serial Monitor)
- [ ] Platform Controller connects to Arduino
- [ ] Servos respond to joystick movement
- [ ] Platform balances object (if applicable)

**Estimated setup time:** 5-15 minutes (depending on driver issues)

---

**Good luck! You've got this! 🚀**
