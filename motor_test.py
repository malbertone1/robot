import RPi.GPIO as GPIO
import time

# Pin definitions
PWM1 = 12  # Left speed
PWM2 = 13  # Right speed
DIR1 = 24  # Left direction
DIR2 = 25  # Right direction

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM1, GPIO.OUT)
GPIO.setup(PWM2, GPIO.OUT)
GPIO.setup(DIR1, GPIO.OUT)
GPIO.setup(DIR2, GPIO.OUT)

# Create PWM instances (frequency 1000Hz)
pwm1 = GPIO.PWM(PWM1, 1000)
pwm2 = GPIO.PWM(PWM2, 1000)
pwm1.start(0)
pwm2.start(0)

try:
    print("Testing forward...")
    GPIO.output(DIR1, GPIO.HIGH)
    GPIO.output(DIR2, GPIO.HIGH)
    pwm1.ChangeDutyCycle(50)  # 50% speed
    pwm2.ChangeDutyCycle(50)
    time.sleep(3)

    print("Stopping...")
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)
    time.sleep(1)

    print("Testing reverse...")
    GPIO.output(DIR1, GPIO.LOW)
    GPIO.output(DIR2, GPIO.LOW)
    pwm1.ChangeDutyCycle(50)
    pwm2.ChangeDutyCycle(50)
    time.sleep(3)

    print("Stopping...")
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
    print("GPIO cleaned up")
