"""
Xbox Controller Joystick Mapper
Reads the right stick from an Xbox controller and maps to roll/pitch angles
"""

from inputs import get_gamepad
import sys
import threading
import time


class ControllerMapper:
    def __init__(self, deadzone=0.08, max_angle=45.0):
        """
        Initialize controller mapper

        Args:
            deadzone: Deadzone threshold (0.0 to 1.0)
            max_angle: Maximum angle in degrees
        """
        self.right_stick_x = 0.0  # Raw value
        self.right_stick_y = 0.0  # Raw value
        self.running = True
        self.deadzone = deadzone
        self.max_angle = max_angle

        # For thread safety
        self._lock = threading.Lock()

    def normalize_axis(self, raw_value, deadzone=None):
        """
        Normalize axis value from raw input to -1.0 to +1.0 range with deadzone

        Args:
            raw_value: Raw controller value (-32768 to 32767)
            deadzone: Deadzone threshold (uses instance default if None)

        Returns:
            Normalized value in range [-1.0, 1.0], or 0.0 if within deadzone
        """
        if deadzone is None:
            deadzone = self.deadzone

        # Normalize to -1.0 to 1.0
        normalized = raw_value / 32768.0

        # Clamp to valid range
        normalized = max(-1.0, min(1.0, normalized))

        # Apply deadzone
        if abs(normalized) < deadzone:
            return 0.0

        # Scale remaining range
        # Map [deadzone, 1.0] to [0.0, 1.0]
        if normalized > 0:
            normalized = (normalized - deadzone) / (1.0 - deadzone)
        else:
            normalized = (normalized + deadzone) / (1.0 - deadzone)

        return normalized

    def get_normalized_values(self):
        """
        Get normalized stick values thread-safely

        Returns:
            Tuple of (x, y) normalized values in range [-1.0, 1.0]
        """
        with self._lock:
            x = self.normalize_axis(self.right_stick_x)
            # Invert Y axis (up is negative on Xbox controllers)
            y = -self.normalize_axis(self.right_stick_y)
            return x, y

    def get_angles(self):
        """
        Get roll and pitch angles in degrees

        Returns:
            Tuple of (roll, pitch) in degrees
        """
        x, y = self.get_normalized_values()
        roll = x * self.max_angle
        pitch = y * self.max_angle
        return roll, pitch

    def set_deadzone(self, deadzone):
        """Set the deadzone threshold"""
        self.deadzone = max(0.0, min(1.0, deadzone))

    def set_max_angle(self, max_angle):
        """Set the maximum angle"""
        self.max_angle = max(0.0, min(90.0, max_angle))

    def read_controller(self):
        """Background thread to continuously read controller input"""
        try:
            while self.running:
                events = get_gamepad()
                for event in events:
                    with self._lock:
                        # Right stick X-axis (RX)
                        if event.code == 'ABS_RX':
                            self.right_stick_x = event.state
                        # Right stick Y-axis (RY)
                        elif event.code == 'ABS_RY':
                            self.right_stick_y = event.state
        except Exception as e:
            print(f"\nError reading controller: {e}")
            self.running = False

    def stop(self):
        """Stop the controller reading thread"""
        self.running = False

    def run(self):
        """Main loop to display mapped values (for standalone testing)"""
        print("Xbox Controller Mapper - Platform Mode")
        print("=" * 50)
        print("Reading right stick -> Roll/Pitch angles...")
        print("Press Ctrl+C to exit\n")

        # Start background thread to read controller
        controller_thread = threading.Thread(target=self.read_controller, daemon=True)
        controller_thread.start()

        try:
            while self.running:
                roll, pitch = self.get_angles()

                # Format serial command
                command = f"<{roll:.1f},{pitch:.1f}>"

                # Display values (carriage return to overwrite line)
                print(f"\rRoll: {roll:+6.1f}° | Pitch: {pitch:+6.1f}° | Serial: {command}", end='', flush=True)

                time.sleep(0.016)  # ~60 updates per second

        except KeyboardInterrupt:
            print("\n\nExiting...")
            self.running = False


def main():
    """Standalone test mode"""
    try:
        mapper = ControllerMapper()
        mapper.run()
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure your Xbox controller is connected and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
