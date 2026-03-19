from modules.obstacle import Obstacle
import time

obstacle = Obstacle()
obstacle.start_scanning()
print("Warming up LiDAR...")
time.sleep(3)

print("Testing - keep robot still first then lift it")
print()

baseline_samples = []
print("Collecting baseline (keep still)...")
for _ in range(20):
    avg = obstacle.get_average_distance()
    if avg > 0:
        baseline_samples.append(avg)
    time.sleep(0.1)

baseline = sum(baseline_samples) / len(baseline_samples)
print(f"Baseline average distance: {baseline:.0f}mm")
print()
print("Now lift the robot...")

try:
    while True:
        avg = obstacle.get_average_distance()
        diff = avg - baseline
        bar = "#" * int(abs(diff) / 50)
        print(f"Avg dist: {avg:.0f}mm  Diff: {diff:.0f}mm  {bar}")
        time.sleep(0.1)

except KeyboardInterrupt:
    obstacle.cleanup()
    print("Done!")
