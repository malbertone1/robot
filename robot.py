from modules.motors import Motors
from modules.lights import Lights
from modules.audio import Audio
from modules.obstacle import Obstacle
from modules.gyroscope import Gyroscope
import time
import sys

class Robot:
    def __init__(self):
        print("Initializing robot...")
        
        # Initialize all modules
        self.motors = Motors()
        self.lights = Lights()
        self.audio = Audio()
        self.gyro = Gyroscope()
        self.obstacle = Obstacle()
        
        # Robot state
        self.running = False
        self.speed = 0.5
        self.target_heading = 0
        
        print("Robot ready!")

    def start(self):
        """Start robot autonomous operation"""
        print("Starting autonomous mode...")
        self.running = True
        
        # Start LiDAR scanning
        self.obstacle.start_scanning()
        time.sleep(2)  # wait for first scan
        
        # Announce ready
        self.audio.speak("Robot starting")
        
        try:
            self._run_loop()
        except KeyboardInterrupt:
            print("Stopped by user")
        finally:
            self.shutdown()

    def _run_loop(self):
        """Main control loop"""
        while self.running:
            front_dist = self.obstacle.get_front_distance()
            
            # Check front obstacle
            if front_dist < 100:  # less than 10cm
                self._handle_obstacle(front_dist)
            else:
                self._move_forward()
            
            time.sleep(0.1)  # 10Hz control loop

    def _move_forward(self):
        """Move forward with gyroscope correction"""
        # Get gyroscope correction
        correction = self.gyro.get_correction(self.target_heading)
        
        left_speed = self.speed - correction
        right_speed = self.speed + correction
        
        # Apply correction
        self.motors.adjust(left_speed, right_speed)
        self.motors._set_forward_direction()
        
        # Set lights
        self.lights.forward_mode()

    def _handle_obstacle(self, distance):
        """Handle obstacle detection"""
        print(f"Obstacle detected at {distance:.0f}mm!")
        
        # Stop and announce
        self.motors.stop()
        self.lights.stopped_mode()
        self.audio.speak(f"Obstacle detected")
        time.sleep(1)
        
        # Decide direction
        direction = self.obstacle.get_best_direction()
        self.audio.speak(f"Turning {direction}")
        
        # Turn to avoid
        if direction == 'left':
            self.motors.spin_left(0.4)
            self.lights.reverse_mode()
            time.sleep(1)
        else:
            self.motors.spin_right(0.4)
            self.lights.reverse_mode()
            time.sleep(1)
        
        # Reset heading after turn
        self.motors.stop()
        self.gyro.reset_heading()
        self.target_heading = 0

    def shutdown(self):
        """Safe shutdown of all components"""
        print("Shutting down...")
        self.running = False
        self.motors.stop()
        self.lights.all_off()
        self.obstacle.cleanup()
        self.gyro.cleanup()
        self.audio.speak("Shutting down")
        time.sleep(2)
        print("Shutdown complete!")

if __name__ == "__main__":
    robot = Robot()
    robot.start()
