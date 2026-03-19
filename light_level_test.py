from gpiozero import PWMOutputDevice
from time import sleep

front = PWMOutputDevice(16)
rear = PWMOutputDevice(20)

print("Light Level Test")
print("Testing different brightness levels")
print("Ctrl+C to stop")
print()

try:
    levels = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    while True:
        # Test front light
        print("--- FRONT LIGHT ---")
        rear.value = 0
        for level in levels:
            front.value = level
            print(f"Front: {int(level*100)}%")
            sleep(1.5)
        front.value = 0
        sleep(1)

        # Test rear light
        print("--- REAR LIGHT ---")
        front.value = 0
        for level in levels:
            rear.value = level
            print(f"Rear: {int(level*100)}%")
            sleep(1.5)
        rear.value = 0
        sleep(1)

        # Test both together
        print("--- BOTH LIGHTS ---")
        for level in levels:
            front.value = level
            rear.value = level
            print(f"Both: {int(level*100)}%")
            sleep(1.5)
        front.value = 0
        rear.value = 0
        sleep(1)

except KeyboardInterrupt:
    print("Stopped")

finally:
    front.value = 0
    rear.value = 0
    print("Lights off")
