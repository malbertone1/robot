from gpiozero import Motor, PWMOutputDevice
from time import sleep

# Pin definitions using gpiozero
# Motor channels using PWM and direction pins
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

    print("Testing forward...")
    dir1.value = 0  # ? swapped from 1 to 0
    dir2.value = 0  # ? swapped from 1 to 0
    pwm1.value = 0.2
    pwm2.value = 0.2
    sleep(3)

    print("Stopping...")
    pwm1.value = 0
    pwm2.value = 0
    sleep(1)

    print("Testing reverse...")
    dir1.value = 1  # ? swapped from 0 to 1
    dir2.value = 1  # ? swapped from 0 to 1
    pwm1.value = 0.2
    pwm2.value = 0.2
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
