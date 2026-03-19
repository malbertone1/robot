import smbus2
import time

class Gyroscope:
    def __init__(self):
        self.MPU_ADDR = 0x68
        self.PWR_MGMT_1 = 0x6B
        self.GYRO_XOUT_H = 0x43
        
        self.bus = smbus2.SMBus(1)
        self.bus.write_byte_data(
            self.MPU_ADDR,
            self.PWR_MGMT_1,
            0
        )
        
        # Calibration
        self.gyro_z_offset = 0
        self.calibrate()
        
        # Heading tracking
        self.heading = 0
        self.last_time = time.time()

    def calibrate(self, samples=100):
        """Calibrate gyroscope offset at rest"""
        print("Calibrating gyroscope - keep robot still...")
        total = 0
        for _ in range(samples):
            total += self._read_gyro_z()
            time.sleep(0.01)
        self.gyro_z_offset = total / samples
        print(f"Calibration complete - offset: {self.gyro_z_offset:.2f}")

    def _read_word(self, reg):
        high = self.bus.read_byte_data(self.MPU_ADDR, reg)
        low = self.bus.read_byte_data(self.MPU_ADDR, reg + 1)
        val = (high << 8) + low
        if val >= 0x8000:
            val = -((65535 - val) + 1)
        return val

    def _read_gyro_z(self):
        return self._read_word(self.GYRO_XOUT_H + 4) / 131.0

    def update_heading(self):
        """Update heading based on gyroscope"""
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        gyro_z = self._read_gyro_z() - self.gyro_z_offset
        self.heading += gyro_z * dt
        return self.heading

    def get_correction(self, target_heading=0):
        """Get correction factor for straight line"""
        heading = self.update_heading()
        error = target_heading - heading
        
        # Simple proportional correction
        correction = error * 0.01
        return correction

    def reset_heading(self):
        """Reset heading to zero"""
        self.heading = 0
        self.last_time = time.time()

    def cleanup(self):
        self.bus.close()
