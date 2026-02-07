# Testing Checklist

## Pre-Flight Checks

- [x] All Python files created and syntax validated
- [x] Dependencies installed (inputs, pyserial)
- [x] Virtual environment configured
- [x] run.bat updated to launch main.py
- [x] README.md documentation complete

## Component Testing

### 1. Controller Input Testing

**Test: Standalone Controller Mapper**
```bash
python controller_mapper.py
```

Expected behavior:
- [ ] Application starts without errors
- [ ] Console shows "Reading right stick -> Roll/Pitch angles..."
- [ ] Moving right stick updates roll/pitch values
- [ ] Values range from -45° to +45° (default max angle)
- [ ] Center position shows approximately 0°, 0°
- [ ] Deadzone prevents small drift (center should stay at 0°)
- [ ] Ctrl+C exits cleanly

### 2. Response Curves Testing

**Test: Each Curve Type**

Linear:
- [ ] Direct 1:1 mapping
- [ ] Full stick deflection = ±45°
- [ ] No transformation applied

Exponential (exponent = 2.0):
- [ ] More precise control near center
- [ ] Faster response at edges
- [ ] Smooth acceleration

Ease-In:
- [ ] Slow start from center
- [ ] Fast approach to maximum

Ease-Out:
- [ ] Fast start from center
- [ ] Gentle approach to maximum

Ease-In-Out:
- [ ] Slow at center
- [ ] Fast in middle
- [ ] Slow at maximum

Velocity-Based:
- [ ] Smooths rapid movements
- [ ] Adds inertia effect
- [ ] Continues moving briefly after stick stops

Custom Power:
- [ ] Adjustable S-curve behavior
- [ ] Center bias affects inflection point
- [ ] Curve strength controls steepness

### 3. GUI Testing

**Test: GUI Launch**
```bash
python main.py
```

Expected behavior:
- [ ] Window opens with title "Platform Controller - Xbox to Arduino"
- [ ] Window size is 600x700 pixels
- [ ] Three main sections visible:
  - Platform Visualization (top)
  - Response Curve Settings (middle)
  - Serial Settings (bottom)

**Test: Platform Visualization**
- [ ] Canvas shows dark background (#2b2b2b)
- [ ] Horizon and center lines visible
- [ ] Platform (blue polygon) renders correctly
- [ ] Moving right stick tilts platform in real-time
- [ ] Roll label updates (left/right movement)
- [ ] Pitch label updates (up/down movement)
- [ ] Serial command label shows correct format: `<roll,pitch>`
- [ ] Visualization runs smoothly (no lag or flickering)

**Test: Curve Controls**
- [ ] Curve Type dropdown shows all 7 curve types
- [ ] Selecting different curves changes behavior immediately
- [ ] Max Angle slider (0-90°):
  - [ ] Starts at 45°
  - [ ] Label updates when moved
  - [ ] Affects maximum tilt angle
- [ ] Deadzone slider (0-0.3):
  - [ ] Starts at 0.08
  - [ ] Label updates when moved
  - [ ] Affects center dead zone
- [ ] Parameter section changes based on curve type:
  - Linear: "No adjustable parameters"
  - Exponential: Shows exponent slider (1.0-3.0)
  - Velocity-Based: Shows max velocity slider (10-500°/s)
  - Custom Power: Shows strength and bias sliders

**Test: Serial Settings**
- [ ] Port dropdown shows "Test Mode" by default
- [ ] Connect button works
- [ ] Status indicator turns green when connected to Test Mode
- [ ] Status label shows "Test Mode (No Serial)"
- [ ] Refresh button updates port list
- [ ] If COM ports available, they appear in dropdown

### 4. Serial Communication Testing

**Test: Mock Mode (Test Mode)**
- [ ] Select "Test Mode" from dropdown
- [ ] Click "Connect"
- [ ] Status indicator turns green
- [ ] Moving stick prints commands to console (if mock_mode configured)
- [ ] No actual serial communication occurs

**Test: Real Serial Port (if Arduino connected)**
- [ ] Connect Arduino via USB
- [ ] Click "Refresh" button
- [ ] Arduino COM port appears in dropdown
- [ ] Select Arduino COM port
- [ ] Click "Connect"
- [ ] Status indicator turns green
- [ ] Status shows "Connected to COM#"
- [ ] Open Arduino Serial Monitor at 9600 baud
- [ ] Move controller stick
- [ ] Serial monitor shows commands: `<roll,pitch>`
- [ ] Values update in real-time
- [ ] Click "Disconnect" disconnects cleanly
- [ ] Closing GUI sends neutral position `<0.0,0.0>`

### 5. Integration Testing

**Test: Complete Workflow**
1. [ ] Launch application with `run.bat`
2. [ ] Window opens successfully
3. [ ] Controller detected automatically
4. [ ] Start in Test Mode
5. [ ] Move right stick - platform tilts
6. [ ] Change to Exponential curve
7. [ ] Adjust exponent parameter
8. [ ] Observe difference in response
9. [ ] Change max angle to 30°
10. [ ] Verify platform limits to ±30°
11. [ ] Increase deadzone to 0.15
12. [ ] Verify larger dead zone near center
13. [ ] Try all curve types
14. [ ] Connect to Arduino (if available)
15. [ ] Verify commands received
16. [ ] Close window
17. [ ] Verify cleanup messages

### 6. Edge Case Testing

**Test: Extreme Values**
- [ ] Max angle = 0°: No movement
- [ ] Max angle = 90°: Full range
- [ ] Deadzone = 0.0: Very sensitive
- [ ] Deadzone = 0.3: Large dead zone
- [ ] Rapid stick movements: Smooth response
- [ ] Holding stick at extreme: Stays at max angle

**Test: Error Conditions**
- [ ] No controller connected: Graceful error message
- [ ] Controller disconnected mid-session: Thread exits safely
- [ ] Invalid COM port: Connection fails with message
- [ ] Serial disconnected during use: GUI shows disconnected

**Test: Thread Safety**
- [ ] Rapidly change curve types: No crashes
- [ ] Adjust sliders while moving stick: No conflicts
- [ ] Connect/disconnect serial repeatedly: Stable

### 7. Performance Testing

**Test: Responsiveness**
- [ ] GUI updates feel real-time (no noticeable lag)
- [ ] Platform visualization is smooth
- [ ] No stuttering or frame drops
- [ ] CPU usage is reasonable (<10% on modern PC)
- [ ] Memory usage is stable (not increasing over time)

**Test: Long-Running Stability**
- [ ] Run for 5 minutes continuously
- [ ] Move controller throughout test
- [ ] No memory leaks
- [ ] No performance degradation
- [ ] Clean exit after long session

## Arduino Integration Testing

### Arduino Sketch Upload

**Test: Example Sketch**
1. [ ] Copy example Arduino code from README.md
2. [ ] Open Arduino IDE
3. [ ] Select correct board and port
4. [ ] Upload sketch
5. [ ] Open Serial Monitor at 9600 baud
6. [ ] Verify sketch receives commands

### Hardware Control

**Test: Servo Control (if hardware available)**
1. [ ] Wire servos to Arduino (pins 9, 10)
2. [ ] Power servos appropriately
3. [ ] Upload servo control sketch
4. [ ] Connect Python application to Arduino COM port
5. [ ] Move controller
6. [ ] Verify servos move correspondingly
7. [ ] Test with different max angles
8. [ ] Test with different curves
9. [ ] Verify smooth motion
10. [ ] Verify neutral position on exit

## Documentation Testing

**Test: README Accuracy**
- [ ] Installation instructions work
- [ ] Usage instructions are clear
- [ ] All features mentioned work as described
- [ ] Troubleshooting steps are helpful
- [ ] Arduino example code compiles
- [ ] Configuration examples are correct

**Test: Code Comments**
- [ ] All major functions have docstrings
- [ ] Complex algorithms have inline comments
- [ ] Constants are explained in config.py

## Final Verification

- [ ] All core features implemented
- [ ] No syntax errors in any file
- [ ] All dependencies installed
- [ ] Documentation complete
- [ ] Examples work
- [ ] Application is user-friendly
- [ ] Cleanup happens on exit
- [ ] Thread-safe operation verified

## Known Limitations

Document any limitations found during testing:

1. Controller must be connected before application starts
2. Windows-only (batch file, path handling)
3. Single controller support
4. Fixed 20 Hz update rate
5. tkinter GUI (basic styling)

## Recommended Test Environment

- Windows 10/11
- Python 3.7+
- Xbox One/Series controller (wired or Bluetooth)
- Arduino Uno or compatible (for hardware testing)
- 2x SG90 servos (for hardware testing)

## Bug Report Template

If issues found:

**Bug Description:**
- What happened:
- Expected behavior:
- Steps to reproduce:
- Error messages:
- Environment (OS, Python version):
- Controller type:

## Success Criteria

✓ Application launches without errors
✓ Controller input works smoothly
✓ All curve types function correctly
✓ GUI is responsive and updates in real-time
✓ Serial communication works (Test Mode)
✓ Documentation is clear and accurate
✓ Clean exit with proper cleanup
