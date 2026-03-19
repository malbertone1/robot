from modules.motors import Motors
from modules.gyroscope import Gyroscope
import time

motors = Motors()
gyro = Gyroscope()

BASE_SPEED = 0.3
CORRECTION_FACTOR = 0.05

print(f"Testing straight line - correction factor: {CORRECTION_FACTOR}")
print("Robot will move forward for 5 seconds")
print()

try:
    gyro.reset_heading()
    motors._set_forward_direction()

    print("Starting in 2 seconds - place on clear floor!")
    time.sleep(2)

    start_time = time.time()

    while time.time() - start_time < 3:
        heading = gyro.update_heading()
        error = 0 - heading
        correction = error * CORRECTION_FACTOR

        # Swapped correction sign
        left_speed = max(0.15, min(BASE_SPEED + correction, 0.8))
        right_speed = max(0.15, min(BASE_SPEED - correction, 0.8))

        motors.pwm1.value = left_speed
        motors.pwm2.value = right_speed

        print(f"Heading: {heading:6.2f}  Error: {error:6.2f}  Correction: {correction:6.3f}  Left: {left_speed:.3f}  Right: {right_speed:.3f}")
        time.sleep(0.1)

    motors.pwm1.value = 0
    motors.pwm2.value = 0
    print()
    print(f"Final drift: {gyro.heading:.2f} degrees")
    print("Positive = drifted right")
    print("Negative = drifted left")
    print()
    print("If still drifting left  ? increase CORRECTION_FACTOR")
    print("If drifting right       ? decrease CORRECTION_FACTOR")
    print("If oscillating          ? decrease CORRECTION_FACTOR")

except KeyboardInterrupt:
    print("Stopped")

finally:
    motors.pwm1.value = 0
    motors.pwm2.value = 0
    motors.dir1.value = 0
    motors.dir2.value = 0
