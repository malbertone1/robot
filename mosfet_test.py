from gpiozero import PWMOutputDevice
from time import sleep

# MOSFET pins
FRONT_LIGHT = PWMOutputDevice(16)  # Pin 36
REAR_LIGHT = PWMOutputDevice(20)   # Pin 38

# Safety - initialize LOW
FRONT_LIGHT.value = 0
REAR_LIGHT.value = 0

try:
    print("Initializing - GPIO set safe...")
    sleep(2)  # flip switch during this time!

    print("Test 1: Front light ON full brightness")
    FRONT_LIGHT.value = 1.0
    sleep(2)

    print("Test 2: Front light 50%")
    FRONT_LIGHT.value = 0.5
    sleep(2)

    print("Test 3: Front light OFF")
    FRONT_LIGHT.value = 0
    sleep(1)

    print("Test 4: Rear light ON full brightness")
    REAR_LIGHT.value = 1.0
    sleep(2)

    print("Test 5: Rear light 50%")
    REAR_LIGHT.value = 0.5
    sleep(2)

    print("Test 6: Rear light OFF")
    REAR_LIGHT.value = 0
    sleep(1)

    print("Test 7: Both lights slow blink")
    for i in range(5):
        FRONT_LIGHT.value = 1.0
        REAR_LIGHT.value = 1.0
        sleep(0.5)
        FRONT_LIGHT.value = 0
        REAR_LIGHT.value = 0
        sleep(0.5)

    print("Test 8: Forward mode - front full, rear 50% blink")
    FRONT_LIGHT.value = 1.0
    for i in range(5):
        REAR_LIGHT.value = 0.5
        sleep(0.5)
        REAR_LIGHT.value = 0
        sleep(0.5)
    FRONT_LIGHT.value = 0

    print("Test 9: Reverse mode - rear full, front 50% blink")
    REAR_LIGHT.value = 1.0
    for i in range(5):
        FRONT_LIGHT.value = 0.5
        sleep(0.5)
        FRONT_LIGHT.value = 0
        sleep(0.5)
    REAR_LIGHT.value = 0

    print("All tests complete!")

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    FRONT_LIGHT.value = 0
    REAR_LIGHT.value = 0
    print("GPIO cleaned up")
