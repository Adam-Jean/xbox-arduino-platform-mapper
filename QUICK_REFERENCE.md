# Quick Reference Guide

## Quick Start

### Launch Application
```bash
run.bat
# or
python main.py
```

### First Time Setup
1. Connect Xbox controller
2. Run `run.bat`
3. Select "Test Mode" in Serial dropdown
4. Click "Connect"
5. Move right stick to test

## Keyboard Shortcuts

- **Close Window**: Alt+F4 or click X
- **Ctrl+C** in console: Stop application

## Response Curves at a Glance

| Curve Type | Best For | Key Characteristic |
|------------|----------|-------------------|
| **Linear** | Testing, simple control | Direct 1:1 mapping |
| **Exponential** | General use | Precise center, fast edges |
| **Ease-In** | Smooth acceleration | Slow start |
| **Ease-Out** | Responsive center | Fast start, gentle end |
| **Ease-In-Out** | Natural motion | Smooth both ends |
| **Velocity-Based** | Reducing jitter | Simulated inertia |
| **Custom Power** | Fine-tuning | Fully adjustable |

## Common Settings

### For Precise Control
- Curve: Exponential (exponent 2.5-3.0)
- Max Angle: 30°
- Deadzone: 0.10

### For Responsive Control
- Curve: Ease-Out
- Max Angle: 45°
- Deadzone: 0.05

### For Smooth, Cinematic Motion
- Curve: Velocity-Based (velocity 80°/s)
- Max Angle: 40°
- Deadzone: 0.08

### For Wide Range Motion
- Curve: Linear or Exponential (1.5)
- Max Angle: 60-90°
- Deadzone: 0.08

## Serial Command Reference

### Format
```
<roll,pitch>\n
```

### Examples
```
<0.0,0.0>     # Center/neutral
<45.0,0.0>    # Full right
<-45.0,0.0>   # Full left
<0.0,45.0>    # Full forward
<0.0,-45.0>   # Full backward
<22.5,22.5>   # Diagonal
```

### Timing
- Commands sent at 20 Hz (every 50ms)
- Baudrate: 9600 bps

## Arduino Quick Setup

### Minimal Sketch
```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.remove(0, 1);  // Remove '<'
    cmd.remove(cmd.length() - 1);  // Remove '>'
    int comma = cmd.indexOf(',');
    float roll = cmd.substring(0, comma).toFloat();
    float pitch = cmd.substring(comma + 1).toFloat();
    // Use roll and pitch here
  }
}
```

## File Quick Reference

| File | Purpose |
|------|---------|
| `main.py` | Launch this to start |
| `config.py` | Change settings here |
| `platform_gui.py` | GUI code |
| `controller_mapper.py` | Controller input |
| `response_curves.py` | Curve algorithms |
| `serial_output.py` | Serial communication |
| `README.md` | Full documentation |
| `run.bat` | Quick launch |

## Configuration Quick Edits

### Change Default Max Angle
`config.py` line 10:
```python
DEFAULT_MAX_ANGLE = 45.0  # Change to desired value
```

### Change Update Rate
`config.py` line 17:
```python
GUI_UPDATE_RATE = 20  # Increase for faster updates
```

### Change Serial Baudrate
`config.py` line 14:
```python
SERIAL_BAUDRATE = 9600  # Match your Arduino
```

### Change Default Deadzone
`config.py` line 7:
```python
DEFAULT_DEADZONE = 0.08  # Adjust for your controller
```

## Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Controller not detected | Unplug and replug, check Device Manager |
| Platform drifting | Increase deadzone slider |
| Not sensitive enough | Decrease deadzone, try Exponential curve |
| Too jerky | Use Velocity-Based curve |
| Serial not working | Check COM port, close Arduino IDE monitor |
| GUI frozen | Check console for errors, restart |

## Parameter Ranges

| Parameter | Min | Max | Default | Unit |
|-----------|-----|-----|---------|------|
| Max Angle | 0 | 90 | 45 | degrees |
| Deadzone | 0.0 | 0.3 | 0.08 | normalized |
| Exponent | 1.0 | 3.0 | 2.0 | - |
| Max Velocity | 10 | 500 | 100 | °/s |
| Curve Strength | 0.5 | 3.0 | 1.5 | - |
| Center Bias | 0.1 | 0.9 | 0.5 | - |

## Testing Modes

### Test Mode (No Hardware)
1. Select "Test Mode" in dropdown
2. Click "Connect"
3. Green status = ready
4. No serial output
5. Perfect for experimenting with curves

### Serial Monitor Mode
1. Connect Arduino
2. Select COM port
3. Click "Connect"
4. Open Arduino Serial Monitor (9600 baud)
5. See commands in real-time

### Hardware Control Mode
1. Upload Arduino sketch
2. Connect servos
3. Select COM port in app
4. Click "Connect"
5. Control hardware

## Curve Parameter Effects

### Exponential Exponent
- **1.0**: Linear (no effect)
- **1.5**: Slight curve
- **2.0**: Standard quadratic (recommended)
- **2.5**: Strong curve
- **3.0**: Very strong curve

### Velocity Max Velocity
- **10-50 °/s**: Very slow, heavy damping
- **50-150 °/s**: Moderate, smooth motion
- **150-300 °/s**: Fast, light damping
- **300-500 °/s**: Very fast, minimal damping

### Custom Power Curve Strength
- **0.5-1.0**: Gentle S-curve
- **1.0-2.0**: Moderate S-curve
- **2.0-3.0**: Strong S-curve

### Custom Power Center Bias
- **0.1-0.3**: More precision at start
- **0.4-0.6**: Balanced
- **0.7-0.9**: More precision at end

## Command Line Testing

### Test Controller Only
```bash
python controller_mapper.py
```

### Check Syntax
```bash
python -m py_compile *.py
```

### List COM Ports
```python
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.device)
```

## Exit Procedures

### Normal Exit
- Click window X button
- Sends `<0.0,0.0>` to center platform
- Disconnects serial
- Stops controller thread

### Emergency Stop
- Press Ctrl+C in console
- Immediate shutdown
- May not send neutral position

## Tips

### For Best Results
1. Calibrate deadzone first (eliminate drift)
2. Start with Linear curve to understand baseline
3. Try Exponential with exponent 2.0 for general use
4. Adjust max angle before fine-tuning curves
5. Use Test Mode to experiment freely

### Performance Tips
- Close other controller applications
- Use wired connection for lowest latency
- Keep max angle reasonable (<60°) for smooth motion
- Monitor console for errors

### Safety Tips
- Always test with low max angle first
- Use Test Mode before connecting hardware
- Ensure servos are powered correctly
- Verify neutral position before connecting

## Version Information

**Current Implementation:**
- Python 3.x
- inputs 0.5
- pyserial 3.5
- tkinter (built-in)

**Platform:**
- Windows (primary)
- Requires Xbox-compatible controller

## Getting Help

1. Check README.md for detailed documentation
2. Review TESTING_CHECKLIST.md for known issues
3. Read ARCHITECTURE.md for technical details
4. Check console output for error messages

## Updates and Customization

### Add New Curve Type
1. Edit `response_curves.py`
2. Create new class inheriting ResponseCurve
3. Add to factory function
4. Update `config.py` CURVE_TYPES list
5. Add UI controls in `platform_gui.py`

### Change GUI Colors
`platform_gui.py` lines with color codes:
- Canvas background: `bg='#2b2b2b'`
- Platform color: `fill='#4a90e2'`
- Lines: `fill='#444444'`

### Add More Controllers
Extend `controller_mapper.py` to support additional input devices
