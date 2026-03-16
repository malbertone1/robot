import smbus2
import time

# MPU-6050 registers
MPU_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# Initialize
bus = smbus2.SMBus(1)
bus.write_byte_data(MPU_ADDR, PWR_MGMT_1, 0)  # wake up

def read_word(reg):
    high = bus.read_byte_data(MPU_ADDR, reg)
    low = bus.read_byte_data(MPU_ADDR, reg + 1)
    val = (high << 8) + low
    if val >= 0x8000:
        val = -((65535 - val) + 1)
    return val

print("Reading MPU-6050 - press Ctrl+C to stop")
try:
    while True:
        ax = read_word(ACCEL_XOUT_H) / 16384.0
        ay = read_word(ACCEL_XOUT_H + 2) / 16384.0
        az = read_word(ACCEL_XOUT_H + 4) / 16384.0
        gx = read_word(GYRO_XOUT_H) / 131.0
        gy = read_word(GYRO_XOUT_H + 2) / 131.0
        gz = read_word(GYRO_XOUT_H + 4) / 131.0

        print(f"Accel  X:{ax:6.2f}g  Y:{ay:6.2f}g  Z:{az:6.2f}g")
        print(f"Gyro   X:{gx:6.2f}°/s  Y:{gy:6.2f}°/s  Z:{gz:6.2f}°/s")
        print("---")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Stopped!")
finally:
    bus.close()
