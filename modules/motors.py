from gpiozero import PWMOutputDevice
from time import sleep

class Motors:
    def __init__(self):
        # Pin definitions
        self.pwm1 = PWMOutputDevice(12)  # Left speed
        self.pwm2 = PWMOutputDevice(13)  # Right speed
        self.dir1 = PWMOutputDevice(24)  # Left direction
        self.dir2 = PWMOutputDevice(25)  # Right direction
        
        # Robot dimensions (mm)
        self.length = 320
        self.width = 210
        
        # Speed settings
        self.current_speed = 0
        self.max_speed = 0.8      # 80% max for safety
        self.min_speed = 0.2      # minimum to overcome inertia
        self.accel_step = 0.05    # acceleration increment
        self.accel_delay = 0.1    # seconds between steps
        
        # Safety stop
        self.stop()
    def emergency_stop(self):
        """Immediate stop - no gradual deceleration"""
        self.pwm1.value = 0
        self.pwm2.value = 0
        self.dir1.value = 0
        self.dir2.value = 0
        self.current_speed = 0

    def _set_forward_direction(self):
        self.dir1.value = 0
        self.dir2.value = 0

    def _set_reverse_direction(self):
        self.dir1.value = 1
        self.dir2.value = 1

    def accelerate_to(self, target_speed):
        """Gradually accelerate to target speed"""
        # Start from minimum speed to overcome inertia
        if self.current_speed == 0:
            self.pwm1.value = self.min_speed
            self.pwm2.value = self.min_speed
            self.current_speed = self.min_speed
            sleep(0.2)
        
        # Gradually increase to target
        while self.current_speed < target_speed:
            self.current_speed = min(
                self.current_speed + self.accel_step,
                target_speed
            )
            self.pwm1.value = self.current_speed
            self.pwm2.value = self.current_speed
            sleep(self.accel_delay)

    def decelerate_to(self, target_speed):
        """Gradually decelerate to target speed"""
        while self.current_speed > target_speed:
            self.current_speed = max(
                self.current_speed - self.accel_step,
                target_speed
            )
            self.pwm1.value = self.current_speed
            self.pwm2.value = self.current_speed
            sleep(self.accel_delay)

    def forward(self, speed=0.5):
        """Move forward at given speed"""
        self._set_forward_direction()
        self.accelerate_to(min(speed, self.max_speed))

    def reverse(self, speed=0.5):
        """Move reverse at given speed"""
        self._set_reverse_direction()
        self.accelerate_to(min(speed, self.max_speed))

    def stop(self):
        """Gradually stop"""
        self.decelerate_to(0)
        self.pwm1.value = 0
        self.pwm2.value = 0
        self.dir1.value = 0
        self.dir2.value = 0
        self.current_speed = 0

    def turn_left(self, speed=0.4):
        """Turn left - right side faster"""
        self._set_forward_direction()
        self.pwm1.value = speed * 0.3  # left slower
        self.pwm2.value = speed        # right faster

    def turn_right(self, speed=0.4):
        """Turn right - left side faster"""
        self._set_forward_direction()
        self.pwm1.value = speed        # left faster
        self.pwm2.value = speed * 0.3  # right slower

    def spin_left(self, speed=0.4):
        """Spin on spot counter-clockwise"""
        self.dir1.value = 1  # left reverse
        self.dir2.value = 0  # right forward
        self.pwm1.value = speed
        self.pwm2.value = speed

    def spin_right(self, speed=0.4):
        """Spin on spot clockwise"""
        self.dir1.value = 0  # left forward
        self.dir2.value = 1  # right reverse
        self.pwm1.value = speed
        self.pwm2.value = speed

    def adjust(self, left_speed, right_speed):
        """Fine adjust individual side speeds for gyroscope correction"""
        self.pwm1.value = max(0, min(left_speed, self.max_speed))
        self.pwm2.value = max(0, min(right_speed, self.max_speed))

    def cleanup(self):
        """Safe shutdown"""
        self.stop()
