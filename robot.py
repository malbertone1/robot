from modules.motors import Motors
from modules.lights import Lights
from modules.audio import Audio
from modules.obstacle import Obstacle
from modules.gyroscope import Gyroscope
import time

class Robot:
    def __init__(self):
        print("Initializing robot...")
        self.motors = Motors()
        self.lights = Lights()
        self.audio = Audio()
        self.gyro = Gyroscope()
        self.obstacle = Obstacle()
        self.running = False
        self.speed = 0.15
        self.target_heading = 0
        self.recent_distances = []
        self.turning = False
        self.stuck_counter = 0
        self.stuck_max = 20
        print("Robot ready!")

    def start(self):
        print("Starting autonomous mode...")
        self.running = True
        self.obstacle.start_scanning()
        time.sleep(2)
        self.audio.speak("Robot starting")
        try:
            self._run_loop()
        except KeyboardInterrupt:
            print("Stopped by user")
        finally:
            self.shutdown()

    def _run_loop(self):
        while self.running:

            # Check if robot has been lifted
            if self.gyro.is_lifted():
                print("Robot lifted - stopping motors!")
                self.motors.pwm1.value = 0
                self.motors.pwm2.value = 0
                self.audio.speak("Robot lifted")
                time.sleep(1)
                continue

            front_dist = self.obstacle.get_front_distance()

            if front_dist != float('inf'):
                self.recent_distances.append(front_dist)
                if len(self.recent_distances) > 3:
                    self.recent_distances.pop(0)

            safe_dist = min(self.recent_distances) if self.recent_distances else float('inf')

            print(f"Front: {front_dist:.0f}mm  Safe: {safe_dist:.0f}mm  Scans: {len(self.obstacle.scan_data)}")

            if safe_dist == float('inf') or safe_dist > 500:
                self._move_forward()
            else:
                self._handle_obstacle(safe_dist)

            time.sleep(0.05)

    def _move_forward(self):
        try:
            correction = self.gyro.get_correction(self.target_heading)
        except:
            correction = 0

        left_speed = max(0.15, min(self.speed - correction, 0.8))
        right_speed = max(0.15, min(self.speed + correction, 0.8))

        self.motors._set_forward_direction()
        self.motors.pwm1.value = left_speed
        self.motors.pwm2.value = right_speed
        self.lights.forward_mode()

    def _handle_obstacle(self, distance):
        # Cut power IMMEDIATELY
        self.motors.pwm1.value = 0
        self.motors.pwm2.value = 0
        self.motors.dir1.value = 0
        self.motors.dir2.value = 0

        print(f"Obstacle detected at {distance:.0f}mm!")
        self.lights.stopped_mode()
        time.sleep(0.5)

        self.audio.speak("Obstacle detected")
        time.sleep(2)

        direction = self.obstacle.get_best_direction()
        print(f"Turning {direction} until clear...")
        self.audio.speak(f"Turning {direction}")

        # Set turn direction
        if direction == 'left':
            self.motors.dir1.value = 1
            self.motors.dir2.value = 0
        else:
            self.motors.dir1.value = 0
            self.motors.dir2.value = 1

        self.motors.pwm1.value = 0.3
        self.motors.pwm2.value = 0.3
        self.lights.reverse_mode()
        self.turning = True

        # Keep turning until clear checking for stuck
        stuck_count = 0
        while self.running:
            front_dist = self.obstacle.get_front_distance()
            rotation = self.gyro.get_rotation_rate()
            print(f"Turning {direction}... front: {front_dist:.0f}mm rotation: {rotation:.1f}deg/s")

            # Check if lifted during turn
            if self.gyro.is_lifted():
                print("Lifted during turn - stopping!")
                self.motors.pwm1.value = 0
                self.motors.pwm2.value = 0
                self.audio.speak("Robot lifted")
                break

            # Check if stuck - wheels turning but no rotation detected
            if rotation < 0.5:
                stuck_count += 1
                print(f"Possible stuck - count: {stuck_count}")
            else:
                stuck_count = 0

            # If stuck for too long try reversing
            if stuck_count > self.stuck_max:
                print("Stuck detected - trying reverse!")
                self.audio.speak("Stuck, reversing")
                self._emergency_reverse()
                stuck_count = 0
                break

            # Path clear - exit turn
            if front_dist > 500:
                print("Path clear!")
                break

            time.sleep(0.1)

        self.turning = False
        self.motors.pwm1.value = 0
        self.motors.pwm2.value = 0
        time.sleep(0.5)

        self.gyro.reset_heading()
        self.target_heading = 0
        self.recent_distances.clear()
        print("Resuming...")

    def _emergency_reverse(self):
        """Reverse if stuck - check rear clearance first"""
        rear_dist = self.obstacle.get_rear_distance()
        print(f"Rear distance: {rear_dist:.0f}mm")

        if rear_dist > 300:
            print("Reversing...")
            self.audio.speak("Reversing")
            self.motors.dir1.value = 1
            self.motors.dir2.value = 1
            self.motors.pwm1.value = 0.2
            self.motors.pwm2.value = 0.2
            self.lights.reverse_mode()
            time.sleep(1.5)
            self.motors.pwm1.value = 0
            self.motors.pwm2.value = 0
            time.sleep(0.5)
        else:
            print("Rear blocked - cannot reverse!")
            self.audio.speak("Rear blocked")

    def shutdown(self):
        print("Shutting down...")
        self.running = False
        self.motors.pwm1.value = 0
        self.motors.pwm2.value = 0
        self.motors.dir1.value = 0
        self.motors.dir2.value = 0
        self.lights.all_off()
        self.obstacle.cleanup()
        self.gyro.cleanup()
        self.audio.speak("Shutting down")
        time.sleep(2)
        print("Shutdown complete!")

if __name__ == "__main__":
    robot = Robot()
    robot.start()
