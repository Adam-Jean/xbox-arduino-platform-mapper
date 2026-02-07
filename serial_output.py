"""
Serial communication module for Arduino platform control
"""

import serial
import serial.tools.list_ports


class SerialOutput:
    """Handles serial communication with Arduino"""

    def __init__(self, port=None, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None
        self.is_connected = False
        self.mock_mode = False

    def get_available_ports(self):
        """
        Get list of available COM ports

        Returns:
            List of port names (e.g., ['COM3', 'COM4'])
        """
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect(self, port):
        """
        Connect to specified serial port

        Args:
            port: COM port name (e.g., 'COM3')

        Returns:
            True if connected successfully, False otherwise
        """
        try:
            if self.is_connected:
                self.disconnect()

            self.port = port
            self.serial_connection = serial.Serial(
                port=port,
                baudrate=self.baudrate,
                timeout=1.0
            )
            self.is_connected = True
            print(f"Connected to {port}")
            return True

        except serial.SerialException as e:
            print(f"Failed to connect to {port}: {e}")
            self.is_connected = False
            return False

    def disconnect(self):
        """Disconnect from serial port"""
        if self.serial_connection and self.is_connected:
            try:
                # Send neutral position before disconnecting
                self.send_command(0.0, 0.0)
                self.serial_connection.close()
                print(f"Disconnected from {self.port}")
            except Exception as e:
                print(f"Error during disconnect: {e}")
            finally:
                self.is_connected = False
                self.serial_connection = None

    def send_command(self, roll, pitch):
        """
        Send roll/pitch command to Arduino

        Args:
            roll: Roll angle in degrees
            pitch: Pitch angle in degrees

        Format: <roll,pitch>\n
        Example: <12.5,-8.3>\n
        """
        if self.mock_mode:
            # Mock mode - just print instead of sending
            print(f"[MOCK] <{roll:.1f},{pitch:.1f}>")
            return True

        if not self.is_connected or not self.serial_connection:
            return False

        try:
            # Format command string
            command = f"<{roll:.1f},{pitch:.1f}>\n"

            # Send to serial port
            self.serial_connection.write(command.encode('utf-8'))
            return True

        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
            self.is_connected = False
            return False
        except Exception as e:
            print(f"Error sending command: {e}")
            return False

    def enable_mock_mode(self):
        """Enable mock mode for testing without hardware"""
        self.mock_mode = True
        self.is_connected = True  # Pretend we're connected

    def disable_mock_mode(self):
        """Disable mock mode"""
        self.mock_mode = False
        if self.is_connected and not self.serial_connection:
            self.is_connected = False

    def __del__(self):
        """Cleanup on deletion"""
        if self.is_connected:
            self.disconnect()
