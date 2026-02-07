"""
Response curve system for transforming controller input
"""

import math
import time


class ResponseCurve:
    """Base class for response curves"""

    def apply(self, value):
        """
        Apply the curve transformation to a normalized value

        Args:
            value: Input value in range [-1, 1]

        Returns:
            Transformed value in range [-1, 1]
        """
        raise NotImplementedError

    def get_parameters(self):
        """Return dict of parameter names and current values"""
        return {}

    def set_parameter(self, name, value):
        """Set a parameter value"""
        pass

    def reset(self):
        """Reset any stateful information"""
        pass


class LinearCurve(ResponseCurve):
    """Direct linear mapping - no transformation"""

    def apply(self, value):
        return value


class ExponentialCurve(ResponseCurve):
    """Exponential curve for more precise center control"""

    def __init__(self, exponent=2.0):
        self.exponent = exponent

    def apply(self, value):
        """Apply exponential curve: sign(x) * |x|^exponent"""
        if value == 0:
            return 0
        return math.copysign(abs(value) ** self.exponent, value)

    def get_parameters(self):
        return {"exponent": self.exponent}

    def set_parameter(self, name, value):
        if name == "exponent":
            self.exponent = max(1.0, min(3.0, value))


class EaseInCurve(ResponseCurve):
    """Ease-in curve - slow start, fast end"""

    def apply(self, value):
        """Quadratic ease-in"""
        sign = 1 if value >= 0 else -1
        normalized = abs(value)
        return sign * (normalized ** 2)


class EaseOutCurve(ResponseCurve):
    """Ease-out curve - fast start, slow end"""

    def apply(self, value):
        """Quadratic ease-out"""
        sign = 1 if value >= 0 else -1
        normalized = abs(value)
        return sign * (1 - (1 - normalized) ** 2)


class EaseInOutCurve(ResponseCurve):
    """Ease-in-out curve - slow at both ends"""

    def apply(self, value):
        """Cubic ease-in-out"""
        sign = 1 if value >= 0 else -1
        normalized = abs(value)

        if normalized < 0.5:
            return sign * (4 * normalized ** 3)
        else:
            return sign * (1 - ((-2 * normalized + 2) ** 3) / 2)


class VelocityBasedCurve(ResponseCurve):
    """Velocity-limited curve with inertia simulation"""

    def __init__(self, max_velocity=100.0, acceleration=200.0):
        self.max_velocity = max_velocity  # degrees per second
        self.acceleration = acceleration  # degrees per second squared
        self.current_output = 0.0
        self.last_time = None

    def apply(self, value):
        """Apply velocity limiting"""
        current_time = time.time()

        # Initialize on first call
        if self.last_time is None:
            self.last_time = current_time
            self.current_output = value
            return value

        # Calculate time delta
        dt = current_time - self.last_time
        self.last_time = current_time

        # Avoid division by zero
        if dt <= 0 or dt > 0.1:  # Skip large time gaps
            return self.current_output

        # Calculate difference
        diff = value - self.current_output

        # Calculate max change based on velocity and acceleration
        max_change = self.max_velocity * dt

        # Apply acceleration limiting
        if abs(diff) > max_change:
            diff = math.copysign(max_change, diff)

        # Update output
        self.current_output += diff
        self.current_output = max(-1.0, min(1.0, self.current_output))

        return self.current_output

    def get_parameters(self):
        return {
            "max_velocity": self.max_velocity,
            "acceleration": self.acceleration
        }

    def set_parameter(self, name, value):
        if name == "max_velocity":
            self.max_velocity = max(10.0, min(500.0, value))
        elif name == "acceleration":
            self.acceleration = max(50.0, min(1000.0, value))

    def reset(self):
        """Reset state"""
        self.current_output = 0.0
        self.last_time = None


class CustomPowerCurve(ResponseCurve):
    """Custom power curve with adjustable S-curve characteristics"""

    def __init__(self, curve_strength=1.5, center_bias=0.5):
        self.curve_strength = curve_strength  # 1.0 = linear, higher = more S-curve
        self.center_bias = center_bias  # 0.5 = symmetric, <0.5 = more at start, >0.5 = more at end

    def apply(self, value):
        """Apply custom power curve"""
        if value == 0:
            return 0

        sign = 1 if value >= 0 else -1
        normalized = abs(value)

        # Apply asymmetric power curve
        if normalized < self.center_bias:
            # First half
            t = normalized / self.center_bias
            result = self.center_bias * (t ** self.curve_strength)
        else:
            # Second half
            t = (normalized - self.center_bias) / (1.0 - self.center_bias)
            result = self.center_bias + (1.0 - self.center_bias) * (t ** (1.0 / self.curve_strength))

        return sign * result

    def get_parameters(self):
        return {
            "curve_strength": self.curve_strength,
            "center_bias": self.center_bias
        }

    def set_parameter(self, name, value):
        if name == "curve_strength":
            self.curve_strength = max(0.5, min(3.0, value))
        elif name == "center_bias":
            self.center_bias = max(0.1, min(0.9, value))


def create_curve(curve_type):
    """Factory function to create curve instances"""
    curves = {
        "Linear": LinearCurve,
        "Exponential": ExponentialCurve,
        "Ease-In": EaseInCurve,
        "Ease-Out": EaseOutCurve,
        "Ease-In-Out": EaseInOutCurve,
        "Velocity-Based": VelocityBasedCurve,
        "Custom Power": CustomPowerCurve
    }

    curve_class = curves.get(curve_type, LinearCurve)
    return curve_class()
