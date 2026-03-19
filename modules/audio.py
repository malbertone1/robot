import subprocess
import threading

class Audio:
    def __init__(self):
        self.speaking = False

    def speak(self, text):
        """Speak text without blocking main thread"""
        if not self.speaking:
            thread = threading.Thread(
                target=self._speak,
                args=(text,)
            )
            thread.daemon = True
            thread.start()

    def _speak(self, text):
        """Actually speak using espeak"""
        self.speaking = True
        subprocess.run(
            ['espeak', '-v', 'en', '-s', '150', text],
            capture_output=True
        )
        self.speaking = False

    def cleanup(self):
        pass
