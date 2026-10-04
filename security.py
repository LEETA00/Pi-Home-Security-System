"""Raspberry Pi motion-triggered security camera.
HC-SR04 ultrasonic sensor watches a distance; when something comes closer than
the threshold, the Pi camera captures a photo and logs the event."""
import csv, time, os
from datetime import datetime
from gpiozero import DistanceSensor, Buzzer
from picamera2 import Picamera2

TRIGGER, ECHO, BUZZER_PIN = 23, 24, 17
THRESHOLD_M = 1.0      # alert when something is closer than this (metres)
COOLDOWN_S = 10        # minimum seconds between captures
OUT_DIR = "captures"

os.makedirs(OUT_DIR, exist_ok=True)
sensor = DistanceSensor(echo=ECHO, trigger=TRIGGER, max_distance=4)
buzzer = Buzzer(BUZZER_PIN)
cam = Picamera2()
cam.configure(cam.create_still_configuration())
cam.start()
time.sleep(2)  # let the sensor settle

def log(ts, dist, path):
    new = not os.path.exists("events.csv")
    with open("events.csv", "a", newline="") as f:
        w = csv.writer(f)
        if new: w.writerow(["time", "distance_m", "photo"])
        w.writerow([ts, round(dist, 2), path])

print("Monitoring. Ctrl+C to stop.")
last = 0
try:
    while True:
        d = sensor.distance
        if d < THRESHOLD_M and time.time() - last > COOLDOWN_S:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = f"{OUT_DIR}/intruder_{ts}.jpg"
            cam.capture_file(path)
            buzzer.beep(0.2, 0.2, n=3, background=True)
            log(ts, d, path)
            print(f"[{ts}] Motion at {d:.2f} m -> {path}")
            last = time.time()
        time.sleep(0.2)
except KeyboardInterrupt:
    pass
finally:
    cam.stop()