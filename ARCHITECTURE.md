# System Architecture

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         MAIN APPLICATION                         │
│                           (main.py)                              │
└───────────────────┬─────────────────────┬───────────────────────┘
                    │                     │
                    ▼                     ▼
        ┌───────────────────┐   ┌──────────────────┐
        │  Controller       │   │  Serial Output   │
        │  Mapper           │   │                  │
        │                   │   │  - COM Ports     │
        │  - Read Thread    │   │  - Mock Mode     │
        │  - Normalize      │   │  - Send Commands │
        │  - Deadzone       │   │                  │
        └─────────┬─────────┘   └────────┬─────────┘
                  │                      │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Platform GUI      │
                  │   (platform_gui.py) │
                  │                     │
                  │  ┌───────────────┐  │
                  │  │ Visualization │  │
                  │  │   Canvas      │  │
                  │  └───────────────┘  │
                  │  ┌───────────────┐  │
                  │  │ Curve         │  │
                  │  │ Controls      │  │
                  │  └───────────────┘  │
                  │  ┌───────────────┐  │
                  │  │ Serial        │  │
                  │  │ Settings      │  │
                  │  └───────────────┘  │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Response Curves    │
                  │                     │
                  │  - Linear           │
                  │  - Exponential      │
                  │  - Easing           │
                  │  - Velocity-Based   │
                  │  - Custom Power     │
                  └─────────────────────┘
```

## Data Flow

```
Xbox Controller
       │
       │ (Raw stick values: -32768 to 32767)
       ▼
┌──────────────────┐
│ Controller       │
│ Mapper           │
│                  │
│ 1. Normalize     │ → -1.0 to +1.0
│ 2. Apply         │
│    Deadzone      │ → 0.0 if within threshold
└────────┬─────────┘
         │
         │ (Normalized values: -1.0 to +1.0)
         ▼
┌──────────────────┐
│ Response Curve   │
│                  │
│ Transform        │ → Apply curve function
│ Input            │
└────────┬─────────┘
         │
         │ (Curved values: -1.0 to +1.0)
         ▼
┌──────────────────┐
│ Scale to         │
│ Degrees          │
│                  │
│ value × max_angle│ → -45° to +45° (default)
└────────┬─────────┘
         │
         │ (Angles in degrees)
         ├─────────────────┐
         │                 │
         ▼                 ▼
┌──────────────────┐  ┌──────────────────┐
│ GUI              │  │ Serial Output    │
│ Visualization    │  │                  │
│                  │  │ Format:          │
│ - Draw Platform  │  │ <roll,pitch>\n   │
│ - Update Labels  │  │                  │
└──────────────────┘  └────────┬─────────┘
                               │
                               ▼
                          Arduino
```

## Thread Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         MAIN THREAD                          │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              Tkinter GUI Loop                       │    │
│  │                                                     │    │
│  │  • Platform visualization rendering                │    │
│  │  • Widget event handling                           │    │
│  │  • Update loop (20 Hz)                             │    │
│  │                                                     │    │
│  │  Every 50ms:                                       │    │
│  │    1. Read controller values (thread-safe)         │    │
│  │    2. Apply curve transformation                   │    │
│  │    3. Update visualization                         │    │
│  │    4. Send serial command                          │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      BACKGROUND THREAD                       │
│                      (Daemon Thread)                         │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Controller Reading Loop                    │    │
│  │                                                     │    │
│  │  while running:                                    │    │
│  │    events = get_gamepad()                          │    │
│  │    for event in events:                            │    │
│  │      with lock:                                    │    │
│  │        if event.code == 'ABS_RX':                  │    │
│  │          right_stick_x = event.state               │    │
│  │        elif event.code == 'ABS_RY':                │    │
│  │          right_stick_y = event.state               │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘

Thread Synchronization:
  • threading.Lock() protects shared stick values
  • GUI reads values atomically
  • Background thread writes values atomically
  • No race conditions or data corruption
```

## Class Relationships

```
┌─────────────────────┐
│  ControllerMapper   │
│─────────────────────│
│ - right_stick_x     │
│ - right_stick_y     │
│ - deadzone          │
│ - max_angle         │
│ - _lock             │
│─────────────────────│
│ + normalize_axis()  │
│ + get_normalized()  │
│ + get_angles()      │
│ + set_deadzone()    │
│ + set_max_angle()   │
│ + read_controller() │
└─────────────────────┘

┌─────────────────────┐
│  SerialOutput       │
│─────────────────────│
│ - port              │
│ - baudrate          │
│ - serial_connection │
│ - is_connected      │
│ - mock_mode         │
│─────────────────────│
│ + get_ports()       │
│ + connect()         │
│ + disconnect()      │
│ + send_command()    │
│ + enable_mock()     │
└─────────────────────┘

┌─────────────────────┐
│  ResponseCurve      │◄───────────────┐
│─────────────────────│                │
│ + apply()           │                │
│ + get_parameters()  │                │
│ + set_parameter()   │                │
│ + reset()           │                │
└─────────────────────┘                │
         △                              │
         │                              │
         │ (inherits)                   │
         │                              │
    ┌────┴────────────────────┐         │
    │                         │         │
┌───────────────┐  ┌──────────────────┐ │
│ LinearCurve   │  │ ExponentialCurve │ │
└───────────────┘  └──────────────────┘ │
┌───────────────┐  ┌──────────────────┐ │
│ EaseInCurve   │  │ EaseOutCurve     │ │
└───────────────┘  └──────────────────┘ │
┌───────────────┐  ┌──────────────────┐ │
│VelocityBased  │  │ CustomPowerCurve │ │
└───────────────┘  └──────────────────┘ │
                                         │
┌─────────────────────┐                  │
│  PlatformGUI        │                  │
│─────────────────────│                  │
│ - controller     ───┼──► ControllerMapper
│ - serial         ───┼──► SerialOutput
│ - current_curve  ───┼──────────────────┘
│ - canvas            │
│ - widgets           │
│─────────────────────│
│ + draw_platform()   │
│ + update_loop()     │
│ + on_curve_change() │
│ + cleanup()         │
└─────────────────────┘
```

## Configuration Management

```
┌─────────────────────┐
│     config.py       │
│─────────────────────│
│                     │
│ Constants:          │
│  • DEFAULT_DEADZONE │
│  • DEFAULT_MAX_ANGLE│
│  • SERIAL_BAUDRATE  │
│  • GUI_UPDATE_RATE  │
│  • CURVE_TYPES[]    │
│  • etc.             │
└──────────┬──────────┘
           │
           │ (imported by)
           │
    ┌──────┴─────────────────────┐
    │                            │
    ▼                            ▼
┌──────────────┐         ┌──────────────┐
│ main.py      │         │ platform_gui │
│ serial_output│         │ response_curves
│ etc.         │         │ etc.         │
└──────────────┘         └──────────────┘
```

## Update Timing

```
Controller Thread (continuous):
│
├─ Read gamepad events
├─ Update stick values
└─ Repeat immediately

GUI Thread (20 Hz / 50ms):
│
├─ Read normalized values
├─ Apply response curve
├─ Calculate angles
├─ Draw visualization
├─ Update labels
├─ Send serial command
└─ Wait 50ms → Repeat
```

## Serial Protocol

```
Format: <roll,pitch>\n

Example Messages:
  <0.0,0.0>\n         Center position
  <45.0,0.0>\n        Full right roll
  <0.0,-30.5>\n       Pitch up 30.5°
  <-22.3,15.7>\n      Left roll, pitch down

Parsing on Arduino:
  1. Wait for serial data
  2. Read until '\n'
  3. Remove '<' and '>'
  4. Split on ','
  5. Convert to float
  6. Map to servo angles
  7. Write to servos
```

## Error Handling

```
Controller Errors:
  • Controller disconnected
    → Running flag set to False
    → Thread exits gracefully
    → GUI shows last known values

Serial Errors:
  • Port not available
    → Connection fails, status shown in GUI
    → User can retry or use Test Mode
  • Connection lost during operation
    → is_connected flag cleared
    → GUI shows disconnected status

GUI Errors:
  • Window closed
    → on_closing() handler called
    → Sends neutral position <0.0,0.0>
    → Disconnects serial
    → Stops controller thread
    → Exits cleanly
```

## Extension Points

### Adding New Response Curves

1. Create class inheriting from `ResponseCurve`
2. Implement `apply()` method
3. Optionally implement parameters methods
4. Add to factory in `response_curves.py`
5. Add to `CURVE_TYPES` in `config.py`
6. Add UI controls in `platform_gui.py`

### Adding New Output Methods

1. Create class similar to `SerialOutput`
2. Implement `send_command()` method
3. Initialize in `main.py`
4. Pass to GUI
5. Add UI controls if needed

### Adding More Axes

1. Extend `ControllerMapper` for additional axes
2. Update `PlatformGUI` for more parameters
3. Modify serial protocol format
4. Update Arduino sketch to handle more values
