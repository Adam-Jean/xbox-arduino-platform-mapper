"""
Platform GUI - Visual interface for Xbox controller to Arduino mapper
"""

import tkinter as tk
from tkinter import ttk
import math
import time
from config import *
from response_curves import create_curve


class PlatformGUI:
    def __init__(self, root, controller_mapper, serial_output):
        """
        Initialize the GUI

        Args:
            root: Tkinter root window
            controller_mapper: ControllerMapper instance
            serial_output: SerialOutput instance
        """
        self.root = root
        self.controller = controller_mapper
        self.serial = serial_output

        # Current state
        self.roll = 0.0
        self.pitch = 0.0
        self.current_curve = create_curve("Linear")

        # Velocity control state
        self.control_mode = "Velocity Control (Rate)"  # Default to velocity mode
        self.control_speed = DEFAULT_CONTROL_SPEED
        self.last_update_time = None

        # Velocity acceleration state
        self.roll_hold_time = 0.0  # How long roll has been held in current direction
        self.pitch_hold_time = 0.0  # How long pitch has been held in current direction
        self.last_roll_sign = 0  # Track direction changes (0, 1, -1)
        self.last_pitch_sign = 0

        # Acceleration parameters (user-adjustable)
        self.acceleration_rate = DEFAULT_ACCELERATION_RATE
        self.acceleration_exponent = DEFAULT_ACCELERATION_EXPONENT
        self.max_multiplier = DEFAULT_MAX_MULTIPLIER

        # Setup window
        self.root.title("Platform Controller - Xbox to Arduino")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        # Build UI
        self._build_ui()

        # Start update loop
        self.update_loop()

    def _build_ui(self):
        """Build the user interface"""

        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ===== CONTROL MODE SELECTOR (MOST IMPORTANT!) =====
        mode_frame = ttk.LabelFrame(main_frame, text="⚙️ CONTROL MODE", padding="10")
        mode_frame.pack(fill=tk.X, pady=(0, 10))

        # Control mode selection
        mode_select_frame = ttk.Frame(mode_frame)
        mode_select_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(mode_select_frame, text="Mode:", font=('', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))

        self.mode_var = tk.StringVar(value="Velocity Control (Rate)")
        self.mode_dropdown = ttk.Combobox(
            mode_select_frame,
            textvariable=self.mode_var,
            values=CONTROL_MODES,
            state="readonly",
            width=30,
            font=('', 10)
        )
        self.mode_dropdown.pack(side=tk.LEFT)
        self.mode_dropdown.bind("<<ComboboxSelected>>", self.on_mode_change)

        # Help text
        self.mode_help_label = ttk.Label(
            mode_frame,
            text="🎯 VELOCITY MODE: Joystick controls RATE of change. Hold stick to tilt gradually. Perfect for marble balancing!",
            font=('', 9, 'italic'),
            foreground='#00aa00',
            wraplength=550
        )
        self.mode_help_label.pack(fill=tk.X, pady=(5, 0))

        # Control speed slider (for velocity mode)
        self.speed_frame = ttk.Frame(mode_frame)
        self.speed_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Label(self.speed_frame, text="Control Speed:", width=15).pack(side=tk.LEFT)

        self.control_speed_var = tk.DoubleVar(value=DEFAULT_CONTROL_SPEED)
        self.control_speed_slider = ttk.Scale(
            self.speed_frame,
            from_=MIN_CONTROL_SPEED,
            to=MAX_CONTROL_SPEED,
            orient=tk.HORIZONTAL,
            variable=self.control_speed_var,
            command=self.on_control_speed_change
        )
        self.control_speed_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.control_speed_label = ttk.Label(self.speed_frame, text=f"{DEFAULT_CONTROL_SPEED:.0f}°/s", width=8)
        self.control_speed_label.pack(side=tk.LEFT)

        # Acceleration rate slider
        self.accel_rate_frame = ttk.Frame(mode_frame)
        self.accel_rate_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Label(self.accel_rate_frame, text="Acceleration:", width=15).pack(side=tk.LEFT)

        self.accel_rate_var = tk.DoubleVar(value=DEFAULT_ACCELERATION_RATE)
        self.accel_rate_slider = ttk.Scale(
            self.accel_rate_frame,
            from_=MIN_ACCELERATION_RATE,
            to=MAX_ACCELERATION_RATE,
            orient=tk.HORIZONTAL,
            variable=self.accel_rate_var,
            command=self.on_accel_rate_change
        )
        self.accel_rate_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.accel_rate_label = ttk.Label(self.accel_rate_frame, text=f"{DEFAULT_ACCELERATION_RATE:.2f}", width=8)
        self.accel_rate_label.pack(side=tk.LEFT)

        # Max multiplier slider
        self.max_mult_frame = ttk.Frame(mode_frame)
        self.max_mult_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Label(self.max_mult_frame, text="Max Speed Boost:", width=15).pack(side=tk.LEFT)

        self.max_mult_var = tk.DoubleVar(value=DEFAULT_MAX_MULTIPLIER)
        self.max_mult_slider = ttk.Scale(
            self.max_mult_frame,
            from_=1.0,
            to=5.0,
            orient=tk.HORIZONTAL,
            variable=self.max_mult_var,
            command=self.on_max_mult_change
        )
        self.max_mult_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.max_mult_label = ttk.Label(self.max_mult_frame, text=f"{DEFAULT_MAX_MULTIPLIER:.1f}x", width=8)
        self.max_mult_label.pack(side=tk.LEFT)

        # ===== Platform Visualization =====
        viz_frame = ttk.LabelFrame(main_frame, text="Platform Visualization", padding="10")
        viz_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Canvas for drawing
        self.canvas = tk.Canvas(viz_frame, width=WINDOW_WIDTH-40, height=300, bg='#2b2b2b', highlightthickness=0)
        self.canvas.pack()

        # Value display
        value_frame = ttk.Frame(viz_frame)
        value_frame.pack(fill=tk.X, pady=(10, 0))

        self.roll_label = ttk.Label(value_frame, text="Roll: +0.0°", font=('Courier', 12, 'bold'))
        self.roll_label.pack(side=tk.LEFT, padx=20)

        self.pitch_label = ttk.Label(value_frame, text="Pitch: +0.0°", font=('Courier', 12, 'bold'))
        self.pitch_label.pack(side=tk.LEFT, padx=20)

        self.serial_label = ttk.Label(value_frame, text="Serial: <0.0,0.0>", font=('Courier', 10))
        self.serial_label.pack(side=tk.LEFT, padx=20)

        self.multiplier_label = ttk.Label(
            value_frame,
            text="Speed: 1.0x",
            font=('Courier', 10),
            foreground='#666666'
        )
        self.multiplier_label.pack(side=tk.LEFT, padx=20)

        # ===== Response Curve Settings (only for Position Control) =====
        self.curve_frame = ttk.LabelFrame(main_frame, text="Response Curve Settings (Position Mode Only)", padding="10")
        # Don't pack it yet - will be shown/hidden based on mode

        # Curve type selection
        curve_select_frame = ttk.Frame(self.curve_frame)
        curve_select_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(curve_select_frame, text="Curve Type:").pack(side=tk.LEFT, padx=(0, 10))

        self.curve_var = tk.StringVar(value="Linear")
        self.curve_dropdown = ttk.Combobox(
            curve_select_frame,
            textvariable=self.curve_var,
            values=CURVE_TYPES,
            state="readonly",
            width=20
        )
        self.curve_dropdown.pack(side=tk.LEFT)
        self.curve_dropdown.bind("<<ComboboxSelected>>", self.on_curve_change)

        # Max angle slider
        angle_frame = ttk.Frame(self.curve_frame)
        angle_frame.pack(fill=tk.X, pady=5)

        ttk.Label(angle_frame, text="Max Angle (Global):", width=16).pack(side=tk.LEFT)

        self.max_angle_var = tk.DoubleVar(value=DEFAULT_MAX_ANGLE)
        self.max_angle_slider = ttk.Scale(
            angle_frame,
            from_=MIN_MAX_ANGLE,
            to=MAX_MAX_ANGLE,
            orient=tk.HORIZONTAL,
            variable=self.max_angle_var,
            command=self.on_max_angle_change
        )
        self.max_angle_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.max_angle_label = ttk.Label(angle_frame, text=f"{DEFAULT_MAX_ANGLE:.0f}°", width=6)
        self.max_angle_label.pack(side=tk.LEFT)

        # Help text for max angle
        ttk.Label(
            self.curve_frame,
            text="Limits platform tilt in both Velocity and Position modes",
            font=('', 8, 'italic'),
            foreground='#666666'
        ).pack(pady=(0, 5))

        # Deadzone slider
        deadzone_frame = ttk.Frame(self.curve_frame)
        deadzone_frame.pack(fill=tk.X, pady=5)

        ttk.Label(deadzone_frame, text="Deadzone:", width=12).pack(side=tk.LEFT)

        self.deadzone_var = tk.DoubleVar(value=DEFAULT_DEADZONE)
        self.deadzone_slider = ttk.Scale(
            deadzone_frame,
            from_=0.0,
            to=0.3,
            orient=tk.HORIZONTAL,
            variable=self.deadzone_var,
            command=self.on_deadzone_change
        )
        self.deadzone_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.deadzone_label = ttk.Label(deadzone_frame, text=f"{DEFAULT_DEADZONE:.2f}", width=6)
        self.deadzone_label.pack(side=tk.LEFT)

        # Dynamic parameter frame (changes based on curve type)
        self.param_frame = ttk.Frame(self.curve_frame)
        self.param_frame.pack(fill=tk.X, pady=(10, 0))

        # ===== Serial Settings =====
        self.serial_frame = ttk.LabelFrame(main_frame, text="Serial Settings", padding="10")
        self.serial_frame.pack(fill=tk.X)

        # Port selection
        port_frame = ttk.Frame(self.serial_frame)
        port_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(port_frame, text="Port:").pack(side=tk.LEFT, padx=(0, 10))

        self.port_var = tk.StringVar(value="Test Mode")
        available_ports = self.serial.get_available_ports()
        if not available_ports:
            available_ports = ["No ports found"]

        self.port_dropdown = ttk.Combobox(
            port_frame,
            textvariable=self.port_var,
            values=["Test Mode"] + available_ports,
            state="readonly",
            width=15
        )
        self.port_dropdown.pack(side=tk.LEFT, padx=(0, 10))

        self.connect_button = ttk.Button(port_frame, text="Connect", command=self.toggle_serial_connection)
        self.connect_button.pack(side=tk.LEFT)

        # Refresh ports button
        self.refresh_button = ttk.Button(port_frame, text="Refresh", command=self.refresh_ports)
        self.refresh_button.pack(side=tk.LEFT, padx=(10, 0))

        # Status indicator
        status_frame = ttk.Frame(self.serial_frame)
        status_frame.pack(fill=tk.X)

        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT, padx=(0, 10))

        self.status_canvas = tk.Canvas(status_frame, width=20, height=20, highlightthickness=0)
        self.status_canvas.pack(side=tk.LEFT)
        self.status_indicator = self.status_canvas.create_oval(2, 2, 18, 18, fill='gray', outline='')

        self.status_label = ttk.Label(status_frame, text="Disconnected")
        self.status_label.pack(side=tk.LEFT, padx=(5, 0))

        # Initialize in test mode
        self.serial.enable_mock_mode()
        self.update_status_indicator(True)

    def _build_curve_parameters(self):
        """Build parameter controls for current curve type"""
        # Clear existing widgets
        for widget in self.param_frame.winfo_children():
            widget.destroy()

        curve_type = self.curve_var.get()

        if curve_type == "Linear":
            # No parameters
            ttk.Label(self.param_frame, text="No adjustable parameters", font=('', 9, 'italic')).pack()

        elif curve_type == "Exponential":
            frame = ttk.Frame(self.param_frame)
            frame.pack(fill=tk.X, pady=5)

            ttk.Label(frame, text="Exponent:", width=12).pack(side=tk.LEFT)

            self.exp_var = tk.DoubleVar(value=DEFAULT_EXPONENT)
            exp_slider = ttk.Scale(
                frame,
                from_=MIN_EXPONENT,
                to=MAX_EXPONENT,
                orient=tk.HORIZONTAL,
                variable=self.exp_var,
                command=lambda v: self.on_curve_param_change('exponent', float(v))
            )
            exp_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            self.exp_label = ttk.Label(frame, text=f"{DEFAULT_EXPONENT:.1f}", width=6)
            self.exp_label.pack(side=tk.LEFT)

        elif curve_type == "Velocity-Based":
            # Max velocity parameter
            frame1 = ttk.Frame(self.param_frame)
            frame1.pack(fill=tk.X, pady=5)

            ttk.Label(frame1, text="Max Velocity:", width=12).pack(side=tk.LEFT)

            self.vel_var = tk.DoubleVar(value=DEFAULT_MAX_VELOCITY)
            vel_slider = ttk.Scale(
                frame1,
                from_=10.0,
                to=500.0,
                orient=tk.HORIZONTAL,
                variable=self.vel_var,
                command=lambda v: self.on_curve_param_change('max_velocity', float(v))
            )
            vel_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            self.vel_label = ttk.Label(frame1, text=f"{DEFAULT_MAX_VELOCITY:.0f}°/s", width=8)
            self.vel_label.pack(side=tk.LEFT)

        elif curve_type == "Custom Power":
            # Curve strength
            frame1 = ttk.Frame(self.param_frame)
            frame1.pack(fill=tk.X, pady=5)

            ttk.Label(frame1, text="Curve Strength:", width=12).pack(side=tk.LEFT)

            self.strength_var = tk.DoubleVar(value=1.5)
            strength_slider = ttk.Scale(
                frame1,
                from_=0.5,
                to=3.0,
                orient=tk.HORIZONTAL,
                variable=self.strength_var,
                command=lambda v: self.on_curve_param_change('curve_strength', float(v))
            )
            strength_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            self.strength_label = ttk.Label(frame1, text="1.5", width=6)
            self.strength_label.pack(side=tk.LEFT)

            # Center bias
            frame2 = ttk.Frame(self.param_frame)
            frame2.pack(fill=tk.X, pady=5)

            ttk.Label(frame2, text="Center Bias:", width=12).pack(side=tk.LEFT)

            self.bias_var = tk.DoubleVar(value=0.5)
            bias_slider = ttk.Scale(
                frame2,
                from_=0.1,
                to=0.9,
                orient=tk.HORIZONTAL,
                variable=self.bias_var,
                command=lambda v: self.on_curve_param_change('center_bias', float(v))
            )
            bias_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            self.bias_label = ttk.Label(frame2, text="0.5", width=6)
            self.bias_label.pack(side=tk.LEFT)

        elif curve_type in ["Ease-In", "Ease-Out", "Ease-In-Out"]:
            # No parameters for these
            ttk.Label(self.param_frame, text="No adjustable parameters", font=('', 9, 'italic')).pack()

    def on_mode_change(self, event=None):
        """Handle control mode change"""
        self.control_mode = self.mode_var.get()

        if self.control_mode == "Velocity Control (Rate)":
            # Hide curve settings, show velocity controls
            self.curve_frame.pack_forget()
            self.speed_frame.pack(fill=tk.X, pady=(10, 0))
            self.accel_rate_frame.pack(fill=tk.X, pady=(10, 0))
            self.max_mult_frame.pack(fill=tk.X, pady=(10, 0))
            self.multiplier_label.pack(side=tk.LEFT, padx=20)
            self.mode_help_label.config(
                text="🎯 VELOCITY MODE: Joystick controls RATE of change. Hold stick to tilt gradually. Perfect for marble balancing!",
                foreground='#00aa00'
            )
            # Reset acceleration state
            self.roll_hold_time = 0.0
            self.pitch_hold_time = 0.0
            self.last_roll_sign = 0
            self.last_pitch_sign = 0
        else:
            # Show curve settings, hide velocity controls
            self.curve_frame.pack(fill=tk.X, pady=(0, 10), before=self.serial_frame)
            self.speed_frame.pack_forget()
            self.accel_rate_frame.pack_forget()
            self.max_mult_frame.pack_forget()
            self.multiplier_label.pack_forget()
            self.mode_help_label.config(
                text="📍 POSITION MODE: Joystick position = platform angle directly. More sensitive!",
                foreground='#aa6600'
            )

    def on_control_speed_change(self, value):
        """Handle control speed change"""
        speed = float(value)
        self.control_speed = speed
        self.control_speed_label.config(text=f"{speed:.0f}°/s")

    def on_accel_rate_change(self, value):
        """Handle acceleration rate change"""
        value = float(value)
        self.acceleration_rate = value
        self.accel_rate_label.config(text=f"{value:.2f}")

    def on_max_mult_change(self, value):
        """Handle max multiplier change"""
        value = float(value)
        self.max_multiplier = value
        self.max_mult_label.config(text=f"{value:.1f}x")

    def on_curve_change(self, event=None):
        """Handle curve type change"""
        curve_type = self.curve_var.get()
        self.current_curve = create_curve(curve_type)
        self._build_curve_parameters()

    def on_curve_param_change(self, param_name, value):
        """Handle curve parameter change"""
        self.current_curve.set_parameter(param_name, value)

        # Update label
        if param_name == 'exponent':
            self.exp_label.config(text=f"{value:.1f}")
        elif param_name == 'max_velocity':
            self.vel_label.config(text=f"{value:.0f}°/s")
        elif param_name == 'curve_strength':
            self.strength_label.config(text=f"{value:.1f}")
        elif param_name == 'center_bias':
            self.bias_label.config(text=f"{value:.2f}")

    def on_max_angle_change(self, value):
        """Handle max angle change"""
        angle = float(value)
        self.controller.set_max_angle(angle)
        self.max_angle_label.config(text=f"{angle:.0f}°")

    def on_deadzone_change(self, value):
        """Handle deadzone change"""
        deadzone = float(value)
        self.controller.set_deadzone(deadzone)
        self.deadzone_label.config(text=f"{deadzone:.2f}")

    def toggle_serial_connection(self):
        """Connect or disconnect from serial port"""
        port = self.port_var.get()

        if self.serial.is_connected:
            # Disconnect
            self.serial.disconnect()
            self.serial.disable_mock_mode()
            self.connect_button.config(text="Connect")
            self.update_status_indicator(False)
        else:
            # Connect
            if port == "Test Mode":
                self.serial.enable_mock_mode()
                self.connect_button.config(text="Disconnect")
                self.update_status_indicator(True)
            elif port != "No ports found":
                success = self.serial.connect(port)
                if success:
                    self.connect_button.config(text="Disconnect")
                    self.update_status_indicator(True)
                else:
                    self.update_status_indicator(False)

    def refresh_ports(self):
        """Refresh available COM ports"""
        available_ports = self.serial.get_available_ports()
        if not available_ports:
            available_ports = ["No ports found"]

        self.port_dropdown['values'] = ["Test Mode"] + available_ports

    def update_status_indicator(self, connected):
        """Update the status indicator light"""
        if connected:
            self.status_canvas.itemconfig(self.status_indicator, fill='#00ff00')
            port = self.port_var.get()
            if port == "Test Mode":
                self.status_label.config(text="Test Mode (No Serial)")
            else:
                self.status_label.config(text=f"Connected to {port}")
        else:
            self.status_canvas.itemconfig(self.status_indicator, fill='gray')
            self.status_label.config(text="Disconnected")

    def draw_platform(self, roll, pitch):
        """
        Draw the tilted platform visualization

        Args:
            roll: Roll angle in degrees
            pitch: Pitch angle in degrees
        """
        self.canvas.delete("all")

        # Canvas center
        cx = (WINDOW_WIDTH - 40) // 2
        cy = 150

        # Draw horizon line
        self.canvas.create_line(0, cy, WINDOW_WIDTH-40, cy, fill='#444444', dash=(4, 4))
        self.canvas.create_line(cx, 0, cx, 300, fill='#444444', dash=(4, 4))

        # Convert angles to radians
        roll_rad = math.radians(roll)
        pitch_rad = math.radians(pitch)

        # Platform dimensions
        w = PLATFORM_WIDTH
        h = PLATFORM_HEIGHT

        # Define platform corners (before rotation)
        corners = [
            (-w/2, -h/2, 0),
            (w/2, -h/2, 0),
            (w/2, h/2, 0),
            (-w/2, h/2, 0)
        ]

        # Apply rotations (simplified 3D projection)
        rotated = []
        for x, y, z in corners:
            # Rotate around X-axis (pitch)
            y1 = y * math.cos(pitch_rad) - z * math.sin(pitch_rad)
            z1 = y * math.sin(pitch_rad) + z * math.cos(pitch_rad)

            # Rotate around Y-axis (roll)
            x2 = x * math.cos(roll_rad) + z1 * math.sin(roll_rad)
            z2 = -x * math.sin(roll_rad) + z1 * math.cos(roll_rad)

            # Project to 2D (simple orthographic projection)
            screen_x = cx + x2
            screen_y = cy + y1 - z2 * 0.5  # Z affects Y for depth effect

            rotated.append((screen_x, screen_y))

        # Draw platform
        self.canvas.create_polygon(
            rotated,
            fill='#4a90e2',
            outline='#ffffff',
            width=3
        )

        # Draw center dot
        self.canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill='red', outline='white')

        # Draw angle indicators
        self.canvas.create_text(
            50, 20,
            text=f"Roll: {roll:+.1f}°",
            fill='white',
            font=('Courier', 11),
            anchor='nw'
        )
        self.canvas.create_text(
            50, 40,
            text=f"Pitch: {pitch:+.1f}°",
            fill='white',
            font=('Courier', 11),
            anchor='nw'
        )

    def update_loop(self):
        """Main update loop - called every frame"""
        # Calculate time delta for velocity control
        current_time = time.time()
        if self.last_update_time is None:
            self.last_update_time = current_time
            dt = 0.05  # Default to 50ms for first frame
        else:
            dt = current_time - self.last_update_time
            self.last_update_time = current_time

        # Clamp dt to reasonable values
        dt = max(0.001, min(0.2, dt))

        # Get normalized values from controller
        x, y = self.controller.get_normalized_values()

        if self.control_mode == "Velocity Control (Rate)":
            # VELOCITY CONTROL MODE - Joystick controls rate of change
            # x and y represent the SPEED at which to change the angle

            # Get stick deflection
            x_deflection = x  # -1 to 1
            y_deflection = -y  # Invert Y axis for correct pitch direction

            # Track direction changes for roll
            current_roll_sign = 1 if x_deflection > 0 else (-1 if x_deflection < 0 else 0)
            if current_roll_sign != self.last_roll_sign and current_roll_sign != 0:
                # Direction changed - reset acceleration
                self.roll_hold_time = 0.0
            self.last_roll_sign = current_roll_sign

            # Track direction changes for pitch
            current_pitch_sign = 1 if y_deflection > 0 else (-1 if y_deflection < 0 else 0)
            if current_pitch_sign != self.last_pitch_sign and current_pitch_sign != 0:
                self.pitch_hold_time = 0.0
            self.last_pitch_sign = current_pitch_sign

            # Update hold times if stick is deflected beyond deadzone
            if abs(x_deflection) > 0.01:  # Small threshold to avoid jitter
                self.roll_hold_time += dt
            else:
                self.roll_hold_time = 0.0  # Reset when centered

            if abs(y_deflection) > 0.01:
                self.pitch_hold_time += dt
            else:
                self.pitch_hold_time = 0.0

            # Calculate acceleration multipliers
            # Formula: multiplier = 1.0 + (hold_time^exponent * deflection_factor * accel_rate)
            # deflection_factor: larger stick movements accelerate faster

            roll_deflection_factor = abs(x_deflection)  # 0 to 1
            pitch_deflection_factor = abs(y_deflection)

            # Exponential time component
            roll_time_factor = self.roll_hold_time ** self.acceleration_exponent
            pitch_time_factor = self.pitch_hold_time ** self.acceleration_exponent

            # Calculate multipliers
            roll_multiplier = 1.0 + (roll_time_factor * roll_deflection_factor * self.acceleration_rate)
            pitch_multiplier = 1.0 + (pitch_time_factor * pitch_deflection_factor * self.acceleration_rate)

            # Clamp to max multiplier
            roll_multiplier = min(roll_multiplier, self.max_multiplier)
            pitch_multiplier = min(pitch_multiplier, self.max_multiplier)

            # Calculate base velocity
            roll_base_velocity = x_deflection * self.control_speed
            pitch_base_velocity = y_deflection * self.control_speed

            # Apply acceleration multiplier
            roll_rate = roll_base_velocity * roll_multiplier
            pitch_rate = pitch_base_velocity * pitch_multiplier

            # Update angles
            self.roll += roll_rate * dt
            self.pitch += pitch_rate * dt

            # Clamp to max angle (GLOBAL LIMIT - applies to both modes)
            max_angle = self.controller.max_angle
            self.roll = max(-max_angle, min(max_angle, self.roll))
            self.pitch = max(-max_angle, min(max_angle, self.pitch))

            # Update speed multiplier visual feedback
            current_multiplier = max(roll_multiplier, pitch_multiplier)
            self.multiplier_label.config(text=f"Speed: {current_multiplier:.1f}x")

            # Color code: gray=1x, yellow=1-2x, orange=2-3x
            if current_multiplier < 1.5:
                color = '#666666'
            elif current_multiplier < 2.5:
                color = '#ccaa00'  # Yellow
            else:
                color = '#ff6600'  # Orange
            self.multiplier_label.config(foreground=color)

        else:
            # POSITION CONTROL MODE - Joystick position = angle directly
            # Apply response curve
            x_curved = self.current_curve.apply(x)
            y_curved = self.current_curve.apply(-y)  # Invert Y axis for correct pitch direction

            # Convert to angles
            max_angle = self.controller.max_angle
            self.roll = x_curved * max_angle
            self.pitch = y_curved * max_angle

        # Update display labels
        self.roll_label.config(text=f"Roll: {self.roll:+.1f}°")
        self.pitch_label.config(text=f"Pitch: {self.pitch:+.1f}°")
        self.serial_label.config(text=f"Serial: <{self.roll:.1f},{self.pitch:.1f}>")

        # Draw platform
        self.draw_platform(self.roll, self.pitch)

        # Send to serial
        self.serial.send_command(self.roll, self.pitch)

        # Schedule next update
        update_interval = int(1000 / GUI_UPDATE_RATE)  # Convert Hz to ms
        self.root.after(update_interval, self.update_loop)

    def cleanup(self):
        """Cleanup on exit"""
        # Send neutral position
        self.serial.send_command(0.0, 0.0)
        self.serial.disconnect()
