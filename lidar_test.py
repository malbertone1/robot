from pyrplidar import PyRPlidar
import time

lidar = PyRPlidar()
lidar.connect(port="/dev/ttyUSB0", baudrate=460800, timeout=3)

info = lidar.get_info()
print("Info:", info)

health = lidar.get_health()
print("Health:", health)

time.sleep(2)

print("Starting scan - press Ctrl+C to stop")
try:
    scan_generator = lidar.start_scan()
    current_scan = []
    revolution_count = 0
    
    for scan in scan_generator():
        # Detect revolution wrap
        if current_scan and scan.angle < current_scan[-1].angle:
            revolution_count += 1
            if revolution_count == 2:
                # Now we have one complete revolution
                print(f"\nComplete 360° scan - {len(current_scan)} points")
                for point in current_scan:
                    if point.quality > 0:
                        print(f"Angle: {point.angle:.2f}° Distance: {point.distance:.2f}mm Quality: {point.quality}")
                current_scan = []
                revolution_count = 0
                break
        current_scan.append(scan)

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    lidar.stop()
    lidar.disconnect()
    print("Done!")
