from pyrplidar import PyRPlidar
import threading
import math

class Obstacle:
    def __init__(self):
        # Robot dimensions (mm)
        self.robot_length = 320
        self.robot_width = 210
        self.min_clearance = 100  # 10cm minimum clearance
        
        # Safety zones based on robot size
        self.front_zone = (350, 10)    # ±10° from front
        self.rear_zone = (170, 190)    # around 180°
        self.left_zone = (260, 280)    # around 270°
        self.right_zone = (80, 100)    # around 90°
        
        # Current scan data
        self.scan_data = {}
        self.scanning = False
        self.scan_thread = None
        
        # Connect LiDAR
        self.lidar = PyRPlidar()
        self.lidar.connect(
            port="/dev/ttyUSB0",
            baudrate=460800,
            timeout=3
        )
    def get_rear_distance(self):
        """Get actual rear distance in mm"""
        return self.get_min_distance(170, 190)

    def is_rear_clear(self):
        """Check if rear is clear for reversing"""
        dist = self.get_rear_distance()
        return dist > (self.min_clearance + self.robot_length/2)

    def start_scanning(self):
        """Start background scanning thread"""
        self.scanning = True
        self.scan_thread = threading.Thread(
            target=self._scan_loop
        )
        self.scan_thread.daemon = True
        self.scan_thread.start()

    def _scan_loop(self):
        """Continuous background scan"""
        scan_generator = self.lidar.start_scan()
        current_scan = []
        
        for scan in scan_generator():
            if not self.scanning:
                break
            if current_scan and scan.angle < current_scan[-1].angle:
                # Complete revolution - update scan data
                self.scan_data = {
                    point.angle: point.distance
                    for point in current_scan
                    if point.quality > 0 and point.distance > 0
                }
                current_scan = []
            current_scan.append(scan)

    def get_min_distance(self, angle_start, angle_end):
        """Get minimum distance in angle range"""
        if not self.scan_data:
            return float('inf')
        
        distances = []
        for angle, distance in self.scan_data.items():
            if angle_start <= angle_end:
                if angle_start <= angle <= angle_end:
                    distances.append(distance)
            else:  # wraps around 0
                if angle >= angle_start or angle <= angle_end:
                    distances.append(distance)
        
        return min(distances) if distances else float('inf')

    def is_front_clear(self):
        """Check if front is clear"""
        # Front zone considering robot width
        dist = self.get_min_distance(350, 10)
        return dist > (self.min_clearance + self.robot_length/2)

    def is_left_clear(self):
        """Check if left side is clear"""
        dist = self.get_min_distance(260, 280)
        return dist > (self.min_clearance + self.robot_width/2)

    def is_right_clear(self):
        """Check if right side is clear"""
        dist = self.get_min_distance(80, 100)
        return dist > (self.min_clearance + self.robot_width/2)

    def get_front_distance(self):
        """Get actual front distance in mm"""
        return self.get_min_distance(350, 10)

    def get_best_direction(self):
        """Determine best direction to avoid obstacle"""
        left_dist = self.get_min_distance(260, 280)
        right_dist = self.get_min_distance(80, 100)
        
        if left_dist > right_dist:
            return 'left'
        return 'right'

    def cleanup(self):
        """Safe shutdown"""
        self.scanning = False
        if self.scan_thread:
            self.scan_thread.join(timeout=2)
        self.lidar.stop()
        self.lidar.disconnect()
