import smbus2
import time
import subprocess

ACCEL_THRESHOLD = 0.15
GYRO_THRESHOLD = 10.0
MPU_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

bus = smbus2.SMBus(1)
bus.write_byte_data(MPU_ADDR, PWR_MGMT_1, 0)

def speak(text):
    subprocess.run(
        ['espeak', '-v', 'en-us', '-s', '130', '-p', '50', '-a', '200', text],
        capture_output=True
    )

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

def read_accel():
    ax = read_word(ACCEL_XOUT_H) / 16384.0
    ay = read_word(ACCEL_XOUT_H + 2) / 16384.0
    az = read_word(ACCEL_XOUT_H + 4) / 16384.0
    return ax, ay, az

def read_gyro():
    gx = read_word(GYRO_XOUT_H) / 131.0
    gy = read_word(GYRO_XOUT_H + 2) / 131.0
    gz = read_word(GYRO_XOUT_H + 4) / 131.0
    return gx, gy, gz

# Calibrate at rest
print("Calibrating - keep still...")
speak("Calibrating, keep still")
time.sleep(1)

samples = 100
gx_off = gy_off = gz_off = 0
ax_off = ay_off = az_off = 0

for _ in range(samples):
    ax, ay, az = read_accel()
    gx, gy, gz = read_gyro()
    ax_off += ax
    ay_off += ay
    az_off += az
    gx_off += gx
    gy_off += gy
    gz_off += gz
    time.sleep(0.01)

ax_off /= samples
ay_off /= samples
az_off /= samples
gx_off /= samples
gy_off /= samples
gz_off /= samples

print(f"Calibration done")
print(f"Accel offsets: X={ax_off:.2f} Y={ay_off:.2f} Z={az_off:.2f}")
print(f"Gyro offsets:  X={gx_off:.2f} Y={gy_off:.2f} Z={gz_off:.2f}")
speak("Calibration complete, ready for testing")


last_direction = None
last_spoken = 0
speak_interval = 1.5    # seconds between announcements

print("\nMove the robot in different directions:")
print("Forward/Reverse = X axis")
print("Left/Right = Y axis or Z gyro")
print("Up/Down = Z axis accelerometer")

try:
    while True:
        ax, ay, az = read_accel()
        gx, gy, gz = read_gyro()

        # Remove offsets
        ax -= ax_off
        ay -= ay_off
        az -= az_off
        gx -= gx_off
        gy -= gy_off
        gz -= gz_off

        print(f"Accel X:{ax:6.2f} Y:{ay:6.2f} Z:{az:6.2f} | Gyro X:{gx:6.1f} Y:{gy:6.1f} Z:{gz:6.1f}")

        direction = None

        # Detect rotation from gyroscope
        if abs(gz) > GYRO_THRESHOLD:
            if gz > 0:
                direction = "turning right"
            else:
                direction = "turning left"

        elif abs(gy) > GYRO_THRESHOLD:
            if gy > 0:
                direction = "moving reverse"
            else:
                direction = "moving forward"

        elif abs(gx) > GYRO_THRESHOLD:
            if gx > 0:
                direction = "tilting forward"
            else:
                direction = "tilting back"

        # Detect linear movement from accelerometer
        elif abs(az) > ACCEL_THRESHOLD:
            if az > 0:
                direction = "moving down"
            else:
                direction = "moving up"

        elif abs(ax) > ACCEL_THRESHOLD:
            if ax > 0:
                direction = "moving left"
            else:
                direction = "moving right"

        elif abs(ay) > ACCEL_THRESHOLD:
            if ay > 0:
                direction = "moving right"
            else:
                direction = "moving left"

        # Speak if new direction and enough time passed
        if direction and direction != last_direction:
            current_time = time.time()
            if current_time - last_spoken > speak_interval:
                print(f">>> {direction}")
                speak(direction)
                last_spoken = current_time
                last_direction = direction

        elif not direction:
            last_direction = None

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopped")
    bus.close()
