import smbus2
import time

MPU_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

bus = smbus2.SMBus(1)
bus.write_byte_data(MPU_ADDR, PWR_MGMT_1, 0)

def read_word(reg):
    try:
        high = bus.read_byte_data(MPU_ADDR, reg)
        low = bus.read_byte_data(MPU_ADDR, reg + 1)
        val = (high << 8) + low
        if val >= 0x8000:
            val = -((65535 - val) + 1)
        return val
    except OSError:
        return 0

def read_accel_z():
    return read_word(ACCEL_XOUT_H + 4) / 16384.0

# Calibrate
print("Calibrating - keep still...")
total = 0
for _ in range(100):
    total += read_accel_z()
    time.sleep(0.01)
baseline = total / 100
print(f"Baseline Accel Z: {baseline:.3f}g")
print()
print("Now test different states:")
print("1 - sit still")
print("2 - motors running (run robot.py in another terminal)")
print("3 - lift robot")
print()
print("Press Ctrl+C to stop")
print()

try:
    while True:
        az = read_accel_z()
        diff = abs(az - baseline)
        bar = "#" * int(diff * 20)
        print(f"Accel Z: {az:7.3f}g  Diff from baseline: {diff:.3f}g  {bar}")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Done!")
    bus.close()
