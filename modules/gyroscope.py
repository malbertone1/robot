import smbus2
import time

class Gyroscope:
    def __init__(self):
        self.MPU_ADDR = 0x68
        self.PWR_MGMT_1 = 0x6B
        self.ACCEL_XOUT_H = 0x3B
        self.GYRO_XOUT_H = 0x43

        self.bus = smbus2.SMBus(1)
        self.bus.write_byte_data(
            self.MPU_ADDR,
            self.PWR_MGMT_1,
            0
        )

        # Calibration
        self.gyro_z_offset = 0
        self.accel_z_baseline = 0
        self.calibrate()

        # Heading tracking
        self.heading = 0
        self.last_time = time.time()

        # Stuck detection
        self.last_heading = 0
        self.stuck_threshold = 0.5  # degrees per second minimum when turning
        self.lifted_threshold = 0.3  # g difference from baseline

    def calibrate(self, samples=100):
        print("Calibrating gyroscope - keep robot still...")
        gyro_total = 0
        accel_total = 0
        for _ in range(samples):
            gyro_total += self._read_gyro_z()
            accel_total += self._read_accel_z()
            time.sleep(0.01)
        self.gyro_z_offset = gyro_total / samples
        self.accel_z_baseline = accel_total / samples
        print(f"Calibration complete - gyro offset: {self.gyro_z_offset:.2f} accel baseline: {self.accel_z_baseline:.2f}g")

    def _read_word(self, reg):
        try:
            high = self.bus.read_byte_data(self.MPU_ADDR, reg)
            low = self.bus.read_byte_data(self.MPU_ADDR, reg + 1)
            val = (high << 8) + low
            if val >= 0x8000:
                val = -((65535 - val) + 1)
            return val
        except OSError:
            return 0

    def _read_gyro_z(self):
        return self._read_word(self.GYRO_XOUT_H + 4) / 131.0

    def _read_accel_z(self):
        return self._read_word(self.ACCEL_XOUT_H + 4) / 16384.0

    def update_heading(self):
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        gyro_z = self._read_gyro_z() - self.gyro_z_offset
        self.heading += gyro_z * dt
        return self.heading

    def get_correction(self, target_heading=0):
        try:
            heading = self.update_heading()
            error = target_heading - heading
            correction = error * 0.01
            return correction
        except OSError:
            return 0

    def is_lifted(self):
        """Detect if robot has been lifted"""
        try:
            accel_z = self._read_accel_z()
            difference = abs(accel_z - self.accel_z_baseline)
            if difference > self.lifted_threshold:
                return True
            return False
        except OSError:
            return False

    def is_stuck(self, motors_running):
        """Detect if wheels spinning but robot not moving"""
        try:
            if not motors_running:
                return False
            gyro_z = abs(self._read_gyro_z() - self.gyro_z_offset)
            # If motors running during turn but gyro not detecting rotation
            if gyro_z < self.stuck_threshold:
                return True
            return False
        except OSError:
            return False

    def get_rotation_rate(self):
        """Get current rotation rate in degrees per second"""
        try:
            return abs(self._read_gyro_z() - self.gyro_z_offset)
        except OSError:
            return 0

    def reset_heading(self):
        self.heading = 0
        self.last_time = time.time()

    def cleanup(self):
        self.bus.close()
