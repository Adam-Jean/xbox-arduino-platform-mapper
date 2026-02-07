"""
Configuration constants for the Platform Mapper application
"""

# Controller settings
DEFAULT_DEADZONE = 0.08
CONTROLLER_UPDATE_RATE = 60  # Hz

# Angle limits
DEFAULT_MAX_ANGLE = 45.0  # degrees
MIN_MAX_ANGLE = 0.0
MAX_MAX_ANGLE = 90.0

# Serial settings
SERIAL_BAUDRATE = 9600
SERIAL_TIMEOUT = 1.0

# GUI settings
GUI_UPDATE_RATE = 20  # Hz (50ms)
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700

# Platform visualization
PLATFORM_WIDTH = 200
PLATFORM_HEIGHT = 150
PLATFORM_DEPTH = 20  # Visual depth for 3D effect

# Response curve defaults
DEFAULT_EXPONENT = 2.0
MIN_EXPONENT = 1.0
MAX_EXPONENT = 3.0

DEFAULT_MAX_VELOCITY = 100.0  # degrees per second
DEFAULT_ACCELERATION = 200.0  # degrees per second squared

# Control modes
CONTROL_MODES = [
    "Velocity Control (Rate)",  # Joystick controls speed of change - BEST FOR MARBLE
    "Position Control (Direct)"  # Joystick controls angle directly
]

# Velocity control settings (for marble balancing)
DEFAULT_CONTROL_SPEED = 30.0  # degrees per second at full stick deflection
MIN_CONTROL_SPEED = 5.0
MAX_CONTROL_SPEED = 100.0

# Velocity acceleration settings
DEFAULT_ACCELERATION_RATE = 0.5  # How quickly acceleration builds (higher = faster ramp)
MIN_ACCELERATION_RATE = 0.1
MAX_ACCELERATION_RATE = 2.0

DEFAULT_ACCELERATION_EXPONENT = 1.5  # Exponential curve strength (>1 = exponential growth)
DEFAULT_MAX_MULTIPLIER = 3.0  # Maximum speed multiplier (3x base speed)

# Curve presets (only used in Position Control mode)
CURVE_TYPES = [
    "Linear",
    "Exponential",
    "Ease-In",
    "Ease-Out",
    "Ease-In-Out",
    "Velocity-Based",
    "Custom Power"
]
