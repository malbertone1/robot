from gpiozero import PWMOutputDevice
import threading
from time import sleep

class Lights:
    def __init__(self):
        self.front = PWMOutputDevice(16)
        self.rear = PWMOutputDevice(20)
        self.blinking = False
        self.blink_thread = None
        
        # Safety - start off
        self.all_off()

    def _blink(self, light, brightness, interval):
        """Background blink thread"""
        while self.blinking:
            light.value = brightness
            sleep(interval)
            light.value = 0
            sleep(interval)

    def _stop_blink(self):
        """Stop any active blinking"""
        self.blinking = False
        if self.blink_thread:
            self.blink_thread.join()
            self.blink_thread = None

    def forward_mode(self):
        """Front 100%, rear 20% blinking"""
        self._stop_blink()
        self.front.value = 1.0
        self.rear.value = 0
        self.blinking = True
        self.blink_thread = threading.Thread(
            target=self._blink,
            args=(self.rear, 0.2, 0.5)
        )
        self.blink_thread.daemon = True
        self.blink_thread.start()

    def reverse_mode(self):
        """Rear 100%, front 20% blinking"""
        self._stop_blink()
        self.rear.value = 1.0
        self.front.value = 0
        self.blinking = True
        self.blink_thread = threading.Thread(
            target=self._blink,
            args=(self.front, 0.2, 0.5)
        )
        self.blink_thread.daemon = True
        self.blink_thread.start()

    def stopped_mode(self):
        """Both at 30% steady"""
        self._stop_blink()
        self.front.value = 0.3
        self.rear.value = 0.3

    def all_off(self):
        """All lights off"""
        self._stop_blink()
        self.front.value = 0
        self.rear.value = 0

    def cleanup(self):
        """Safe shutdown"""
        self.all_off()
