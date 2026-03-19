import smbus2
import time

MPU_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B

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
print(f"Baseline: {baseline:.3f}g")
print("Lift robot to test...")

lifted_counter = 0
lifted_threshold = 0.4
lifted_confirmed = 3  # need 3 consecutive readings

try:
    while True:
        samples = []
        for _ in range(5):
            samples.append(read_accel_z())
            time.sleep(0.005)
        avg_z = sum(samples) / len(samples)
        diff = abs(avg_z - baseline)

        if diff > lifted_threshold:
            lifted_counter += 1
        else:
            lifted_counter = max(0, lifted_counter - 1)

        confirmed = lifted_counter >= lifted_confirmed

        print(f"Avg Z: {avg_z:.3f}g  Diff: {diff:.3f}g  Counter: {lifted_counter}  LIFTED: {confirmed}")
        time.sleep(0.1)

except KeyboardInterrupt:
    bus.close()
