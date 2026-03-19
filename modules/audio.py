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
        self.speaking = True
        subprocess.run(
            ['espeak', 
             '-v', 'en-us',  # American English clearer
             '-s', '130',    # slower speed (was 150)
             '-p', '50',     # pitch
             '-a', '200',    # amplitude (louder)
             text],
            capture_output=True
        )
        self.speaking = False

    def cleanup(self):
        pass
