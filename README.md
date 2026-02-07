# Xbox Controller to Arduino Platform Mapper

A complete system that maps Xbox controller input to Arduino-controlled platforms (gimbals, Stewart platforms, marble balancers) with real-time visualization and configurable response curves.

**Perfect for hackathons** - Cross-platform, quick setup, works without hardware in Test Mode.

## Quick Start

**Time to first run: < 5 minutes**

### Windows

```cmd
# Option 1: Download and run
# Download from releases, extract, then:
run.bat

# Option 2: Clone from git
git clone https://github.com/Adam-Jean/xbox-arduino-platform-mapper.git
cd xbox-arduino-platform-mapper
run.bat
```

### Mac

```bash
# Clone or download
git clone https://github.com/Adam-Jean/xbox-arduino-platform-mapper.git
cd xbox-arduino-platform-mapper

# Make executable and run
chmod +x run.sh
./run.sh
```

### Linux

```bash
# Clone or download
git clone https://github.com/Adam-Jean/xbox-arduino-platform-mapper.git
cd xbox-arduino-platform-mapper

# Add user to dialout group (for serial port access)
sudo usermod -a -G dialout $USER
# Log out and log back in after this command

# Make executable and run
chmod +x run.sh
./run.sh
```

**For hackathon participants:** See [HACKATHON_QUICK_START.md](HACKATHON_QUICK_START.md) for condensed setup guide.

## Features

- **Xbox Controller Input**: Maps right analog stick to roll/pitch angles
- **Two Control Modes**:
  - **Velocity Mode**: Joystick acts like a rate control (returns to center)
  - **Position Mode**: Joystick position = platform angle (stays where released)
- **7 Response Curves**: Linear, Quadratic, Cubic, Exponential, S-Curve, and more
- **Real-Time 3D Visualization**: Live platform tilt display with roll/pitch angles
- **Serial Output**: Sends `<roll,pitch>\n` commands to Arduino at 20 Hz
- **Test Mode**: Run without hardware - perfect for testing and development
- **Cross-Platform**: Works on Windows, Mac, and Linux
- **Configurable**: Adjustable max angle, deadzone, acceleration, response curves

## Prerequisites

- **Python 3.7+** (3.8+ recommended)
- **Xbox controller** (USB or Bluetooth)
- **Arduino** (optional - Test Mode works without)

### Platform-Specific Requirements

**Windows:**
- Xbox controller drivers (usually automatic)
- No additional setup needed

**Mac:**
- Xbox controller works natively via USB
- Bluetooth may require third-party drivers

**Linux:**
- Xbox controller: `sudo apt install xboxdrv` or use built-in `xpad` driver
- Serial port access: Add user to `dialout` group (see Quick Start)

## Installation

The `run.bat` (Windows) and `run.sh` (Mac/Linux) scripts automatically:
1. Create a Python virtual environment (if not exists)
2. Install dependencies from `requirements.txt`
3. Launch the application

### Manual Installation

If you prefer manual setup:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

### Dependencies

- `inputs==0.5` - Xbox controller input handling
- `pyserial==3.5` - Serial communication with Arduino

## Test Mode (No Arduino Needed)

**Perfect for:**
- Testing software setup
- Experimenting with response curves
- Demonstrating functionality
- Debugging controller issues

**How to use:**
1. Launch the application
2. Check the "Test Mode" checkbox
3. Click "Connect"
4. Move the right joystick - watch the 3D platform respond

Commands are displayed but not sent to serial port.

## Arduino Integration

### Serial Communication Protocol

**Format:** `<roll,pitch>\n`

**Example:** `<12.5,-8.3>\n`

**Specifications:**
- **Baudrate:** 9600 (configurable in `config.py`)
- **Roll/Pitch Range:** -45.0° to +45.0° (default, adjustable via Max Angle slider)
- **Update Rate:** 20 Hz (50ms interval)
- **Format:** ASCII string, angle-bracket delimited, comma-separated floats

### Arduino Example Sketches

Complete working examples are provided in the `arduino_examples/` directory:

1. **basic_receiver/** - Test serial communication without hardware
2. **servo_control/** - Full servo motor control example

See [arduino_examples/README.md](arduino_examples/README.md) for:
- Wiring diagrams
- Calibration instructions
- Troubleshooting
- Extension examples

### Quick Arduino Setup

1. Open `arduino_examples/basic_receiver/basic_receiver.ino`
2. Upload to your Arduino
3. Close Arduino Serial Monitor (prevents port conflicts)
4. In Platform Controller:
   - Uncheck "Test Mode"
   - Select Arduino port from dropdown
   - Click "Connect"

## Platform-Specific Port Names

**Windows:**
- Format: `COM3`, `COM4`, `COM5`, etc.
- Find in: Device Manager → Ports (COM & LPT)

**Mac:**
- Format: `/dev/cu.usbserial-*` or `/dev/cu.usbmodem-*`
- Use `cu` (callout) not `tty` for Arduino
- List ports: `ls /dev/cu.*`

**Linux:**
- Format: `/dev/ttyUSB0` (FTDI, CH340) or `/dev/ttyACM0` (native USB)
- List ports: `ls /dev/tty*`
- Permissions: Must be in `dialout` group (see Quick Start)

## Driver Installation

**Arduino clones often need drivers:**

- **CH340/CH341** (most common): https://sparks.gogo.co.nz/ch340.html
- **FTDI**: https://ftdichip.com/drivers/vcp-drivers/
- **CP2102/CP2104**: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers

**Download before hackathons** - WiFi may be unreliable!

## GUI Interface

### Platform Visualization (Top)
- Real-time 3D platform tilt display
- Shows current roll and pitch angles
- Displays formatted serial command

### Settings Panel (Middle)

**Control Mode:**
- **Velocity Mode**: Joystick controls tilt rate (returns to center when released)
- **Position Mode**: Joystick position = platform angle (stays tilted)

**Response Curve:**
- **Linear**: Direct 1:1 mapping
- **Quadratic**: Gentle near center, aggressive at edges
- **Cubic**: Very gentle center, very aggressive edges
- **S-Curve**: Smooth acceleration curve
- **Exponential**: Configurable power curve (1.0-3.0)
- **Inverse Exponential**: Opposite of exponential
- **Custom**: Advanced curve with adjustable parameters

**Parameters:**
- **Max Angle**: Maximum tilt angle (0-90°)
- **Deadzone**: Center deadzone to eliminate drift (0.0-0.3)
- **Max Velocity**: Speed limit for Velocity Mode (degrees/second)
- **Acceleration**: How quickly velocity builds up (multiplier)

### Serial Settings (Bottom)
- **Port Selection**: Choose COM port or Test Mode
- **Connect/Disconnect**: Toggle serial connection
- **Refresh**: Update available port list
- **Status Indicator**: Shows connection state

## Control Modes Explained

### Velocity Mode (Default)

**Behavior:**
- Joystick position controls **rate of tilt**
- Platform returns to center when joystick is released
- Includes acceleration system for progressive speed control
- Simulates physics/inertia

**Best for:**
- Marble balancing games
- Self-stabilizing platforms
- Dynamic control scenarios
- Intuitive "driving" feel

**Example:**
- Push joystick right → Platform tilts right at increasing speed
- Release joystick → Platform automatically returns to center

### Position Mode

**Behavior:**
- Joystick position directly controls **platform angle**
- Platform stays at angle when joystick is released
- Immediate response, no acceleration
- 1:1 mapping (with response curve applied)

**Best for:**
- Precise positioning
- Camera gimbals
- Manual angle control
- Direct manipulation

**Example:**
- Push joystick 50% right → Platform tilts 50% of max angle
- Release joystick → Platform stays at that angle

## Response Curves

### Linear
Direct 1:1 mapping. No transformation.
- **Best for:** Testing, simple control

### Quadratic
Formula: `sign(x) × x²`
- **Effect:** Gentle near center, faster at edges
- **Best for:** Smooth control with quick max angles

### Cubic
Formula: `sign(x) × x³`
- **Effect:** Very gentle center, very aggressive edges
- **Best for:** Maximum precision at center, explosive at edges

### S-Curve
Sigmoid-based smooth acceleration
- **Effect:** Smooth throughout, no sudden changes
- **Best for:** Beginners, smooth demonstrations

### Exponential
Formula: `sign(x) × |x|^exponent`
- **Parameter:** Exponent (1.0-3.0)
- **Effect:** Adjustable sensitivity curve
- **Best for:** Fine-tuning specific feel

### Inverse Exponential
Opposite of exponential
- **Effect:** More responsive at center, gentle at edges
- **Best for:** Precision work

### Custom
Highly configurable with multiple parameters
- **Best for:** Advanced users wanting exact feel

## Configuration

Edit `config.py` to customize defaults:

```python
DEFAULT_MAX_ANGLE = 45.0        # Starting max angle (degrees)
DEFAULT_DEADZONE = 0.1          # Starting deadzone (0.0-1.0)
DEFAULT_MAX_VELOCITY = 100.0    # Max velocity in Velocity Mode
DEFAULT_ACCELERATION = 3.0      # Acceleration multiplier
SERIAL_BAUDRATE = 9600          # Serial communication speed
GUI_UPDATE_RATE = 20            # GUI refresh rate (Hz)
```

See [CONFIGURATION.md](CONFIGURATION.md) for detailed configuration options.

## Troubleshooting

### Controller Not Detected

**Windows:**
- Check Device Manager → Xbox Peripherals
- Try different USB port
- Reinstall Xbox controller driver

**Mac:**
- Controller should work natively via USB
- For Bluetooth, install 360Controller driver
- Try: `ls /dev/cu.* ` to see if controller shows up

**Linux:**
- Install driver: `sudo apt install xboxdrv`
- Or use built-in `xpad` kernel module
- Test: `jstest /dev/input/js0`
- Grant permissions: `sudo chmod 666 /dev/input/js0`

**All Platforms:**
- Verify controller works in other games
- Try different USB cable
- Press Xbox button to wake controller
- Close other applications using the controller

### Serial Port Issues

**"Permission Denied" (Linux/Mac):**

```bash
# Linux: Add to dialout group
sudo usermod -a -G dialout $USER
# Log out and log back in

# Mac: Usually not needed, but try:
sudo chmod 666 /dev/cu.usbserial-*

# Quick temporary fix (Linux):
sudo chmod 666 /dev/ttyUSB0
```

**No Ports Available:**
- Unplug Arduino, plug back in
- Click "Refresh" button
- Try different USB cable (many are power-only!)
- Install CH340 driver for Arduino clones
- Check Device Manager (Windows) or `ls /dev/tty*` (Mac/Linux)

**"Port Already in Use":**
- Close Arduino IDE Serial Monitor
- Close other serial programs (PuTTY, screen, minicom)
- Only one program can access serial port at a time
- Restart computer if issue persists

**Arduino Not Responding:**
- Verify correct baudrate (9600 default)
- Re-upload Arduino sketch
- Check Arduino Serial Monitor first (verify sketch works)
- Check wiring (TX/RX not needed for USB serial)

### Platform Drifting

**Cause:** Worn or uncalibrated controller thumbsticks

**Fix:**
1. Increase deadzone: Settings → Deadzone → 0.15-0.25
2. Or use Position Mode instead of Velocity Mode
3. Try different controller

### GUI Not Responding

1. Check console for errors
2. Verify controller is detected (Test Mode)
3. Restart application
4. Check Python version (3.7+ required)

### Servos Jittering

**Causes:**
- Insufficient power supply
- Electrical noise
- Signal wire too long

**Fixes:**
- Use external 5V power supply for servos (not Arduino 5V pin)
- Add 100µF capacitor across servo power pins
- Keep servo signal wires under 12 inches
- Add smoothing in Arduino code (see arduino_examples/)

### Platform Moving Incorrectly

1. **Test serial data first:**
   - Upload `basic_receiver.ino`
   - Open Serial Monitor
   - Verify correct roll/pitch values

2. **Check servo mapping:**
   - Servos expect 0-180°
   - Platform Controller sends -45 to +45°
   - Arduino must map correctly (see examples)

3. **Calibrate center position:**
   - Adjust `ROLL_CENTER` and `PITCH_CENTER` in Arduino code

4. **Try different response curve:**
   - Linear is most predictable for testing

## File Structure

```
xbox-arduino-platform-mapper/
├── venv/                          # Virtual environment (not in git)
├── arduino_examples/              # Arduino example sketches
│   ├── basic_receiver/           # Serial test sketch
│   ├── servo_control/            # Servo control example
│   └── README.md                 # Arduino documentation
├── config.py                      # Configuration constants
├── controller_mapper.py           # Xbox controller input handler
├── response_curves.py             # Response curve implementations
├── serial_output.py               # Serial communication module
├── platform_gui.py                # GUI application
├── main.py                        # Application entry point
├── requirements.txt               # Python dependencies
├── run.bat                        # Windows launcher
├── run.sh                         # Mac/Linux launcher
├── .gitignore                     # Git ignore file
├── LICENSE                        # MIT License
├── README.md                      # This file
├── HACKATHON_QUICK_START.md      # Quick setup guide
├── CONFIGURATION.md               # Detailed configuration
├── ARCHITECTURE.md                # System architecture
└── RESPONSE_CURVES.md            # Response curve mathematics
```

## Hardware Setup

### Required Components

- Arduino Uno, Nano, or Mega
- 2× Servo motors (SG90 or similar for 2-axis control)
- USB cable for Arduino
- External 5V power supply for servos (recommended)
- Breadboard and jumper wires
- Platform mount (3D printed or DIY)

### Example Wiring

```
Roll Servo:
  Signal (Orange) → Arduino Pin 9
  Power (Red)     → External 5V
  Ground (Brown)  → Common GND

Pitch Servo:
  Signal (Orange) → Arduino Pin 10
  Power (Red)     → External 5V
  Ground (Brown)  → Common GND

IMPORTANT: Connect external power supply GND to Arduino GND
```

**Warning:** Do NOT power multiple servos from Arduino 5V pin - use external power supply!

### Calibration

1. Upload `servo_control.ino` to Arduino
2. Center platform mechanically
3. In Platform Controller, set Max Angle = 10° (for safety)
4. Test small movements first
5. Adjust `ROLL_CENTER` and `PITCH_CENTER` in Arduino code if needed
6. Gradually increase Max Angle to desired range
7. Tune `ANGLE_SCALE` for sensitivity

See [arduino_examples/README.md](arduino_examples/README.md) for detailed calibration guide.

## Advanced Usage

### Custom Response Curves

Add your own curve in `response_curves.py`:

```python
class MyCustomCurve(ResponseCurve):
    def apply(self, value):
        # Your transformation here
        return value * 0.5  # Example: half sensitivity

    def get_parameters(self):
        return {}

    def set_parameter(self, name, value):
        pass
```

Register in `CURVE_TYPES` dictionary.

### Standalone Controller Test

Test controller without GUI:

```bash
python controller_mapper.py
```

Prints roll/pitch values to console.

### Changing Update Rate

Edit `config.py`:

```python
GUI_UPDATE_RATE = 30  # Increase to 30 Hz for faster updates
SERIAL_UPDATE_RATE = 50  # Send serial at 50 Hz
```

## Tips for Best Results

1. **Always test with Test Mode first** - Verify software works before debugging hardware
2. **Start with Linear curve** - Understand baseline behavior
3. **Adjust deadzone for your controller** - Every controller is different
4. **Use Velocity Mode for balancing** - More intuitive for dynamic control
5. **Use Position Mode for precision** - Better for camera gimbals
6. **Try Quadratic or S-Curve** - Good general-purpose options
7. **Download drivers before hackathons** - WiFi is unreliable
8. **Bring spare USB cables** - Cable failure is the #1 hardware issue

## Documentation

- **[HACKATHON_QUICK_START.md](HACKATHON_QUICK_START.md)** - Condensed 5-minute setup guide
- **[CONFIGURATION.md](CONFIGURATION.md)** - Detailed configuration options
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and code structure
- **[RESPONSE_CURVES.md](RESPONSE_CURVES.md)** - Mathematics behind response curves
- **[arduino_examples/README.md](arduino_examples/README.md)** - Arduino integration guide

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - See [LICENSE](LICENSE) file for details.

Free to use, modify, and distribute for any purpose including commercial use.

## Credits

**Built with:**
- Python 3
- tkinter (GUI framework)
- inputs (Xbox controller library)
- pyserial (Serial communication)

**Designed for:**
- Hackathons
- Educational projects
- Robotics competitions
- DIY makers

## Support

**Issues or questions?**
- GitHub Issues: https://github.com/Adam-Jean/xbox-arduino-platform-mapper/issues
- Check [HACKATHON_QUICK_START.md](HACKATHON_QUICK_START.md) for common problems
- Review troubleshooting section above

## Version History

**v1.0.0** - Initial hackathon-ready release
- Cross-platform support (Windows, Mac, Linux)
- Two control modes (Velocity and Position)
- 7 response curves
- Arduino examples included
- Comprehensive documentation
