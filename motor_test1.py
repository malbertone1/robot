from gpiozero import PWMOutputDevice
from time import sleep

# Pin definitions
pwm1 = PWMOutputDevice(12)  # Left speed
pwm2 = PWMOutputDevice(13)  # Right speed
dir1 = PWMOutputDevice(24)  # Left direction
dir2 = PWMOutputDevice(25)  # Right direction

# Safety - initialize all pins LOW
pwm1.value = 0
pwm2.value = 0
dir1.value = 0
dir2.value = 0

try:
    print("Initializing - GPIO set safe...")
    sleep(2)

    print("Spinning clockwise...")
    dir1.value = 0  # Left forward
    dir2.value = 1  # Right reverse
    pwm1.value = 0.5
    pwm2.value = 0.5
    sleep(3)

    print("Stopping...")
    pwm1.value = 0
    pwm2.value = 0
    sleep(1)

    print("Spinning counter-clockwise...")
    dir1.value = 1  # Left reverse
    dir2.value = 0  # Right forward
    pwm1.value = 0.5
    pwm2.value = 0.5
    sleep(3)

    print("Stopping...")
    pwm1.value = 0
    pwm2.value = 0
    sleep(1)

    print("Test complete!")

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    pwm1.value = 0
    pwm2.value = 0
    dir1.value = 0
    dir2.value = 0
    print("GPIO cleaned up")
