"""
Xbox Controller to Arduino Platform Mapper
Main application entry point
"""

import tkinter as tk
import threading
import sys
from controller_mapper import ControllerMapper
from serial_output import SerialOutput
from platform_gui import PlatformGUI
from config import *


def main():
    """Main application entry point"""
    print("Xbox Controller to Arduino Platform Mapper")
    print("=" * 50)
    print("Initializing...")

    try:
        # Initialize controller mapper
        print("Setting up controller...")
        controller = ControllerMapper(
            deadzone=DEFAULT_DEADZONE,
            max_angle=DEFAULT_MAX_ANGLE
        )

        # Start controller reading thread
        controller_thread = threading.Thread(
            target=controller.read_controller,
            daemon=True
        )
        controller_thread.start()
        print("Controller thread started")

        # Initialize serial output
        print("Setting up serial communication...")
        serial_output = SerialOutput(baudrate=SERIAL_BAUDRATE)
        print("Serial interface ready")

        # Create GUI
        print("Creating GUI...")
        root = tk.Tk()

        # Initialize GUI with controller and serial
        gui = PlatformGUI(root, controller, serial_output)

        # Setup cleanup on window close
        def on_closing():
            print("\nShutting down...")
            gui.cleanup()
            controller.stop()
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        print("Ready!")
        print("\nGUI Controls:")
        print("- Use right stick on Xbox controller")
        print("- Adjust curve type and parameters in GUI")
        print("- Connect to serial port or use Test Mode")
        print("- Close window to exit\n")

        # Start GUI main loop
        root.mainloop()

    except Exception as e:
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure your Xbox controller is connected")
        print("2. Check that the 'inputs' library is installed")
        print("3. Verify serial port access (if using serial)")
        sys.exit(1)


if __name__ == "__main__":
    main()
