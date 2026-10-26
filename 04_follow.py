# 04_follow.py
# Make the turret follow a colored ball, and measure the delay.
# Needs: pyserial, opencv-python, numpy, and serial_servo.ino running on the Arduino.
# Press q to quit; it then prints the median delay in milliseconds.

import time
import statistics
import cv2
import numpy as np
import serial
import os
SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "delay_results.txt")

# ---- Settings to change -------------------------------------------------
PORT = "COM5"
CAMERA_INDEX = 1
LOWER = np.array([95, 100, 90])    # replace with the final values from 02_color_tracker.py
UPPER = np.array([130, 255, 255])
PAN_SIGN = -1        # if the turret moves AWAY from the ball left/right, change to -1
TILT_SIGN = -1       # if it moves AWAY up/down, change to -1
GAIN = 0.02         # degrees of servo movement per pixel of error (bigger = faster, shakier)
DEAD_ZONE = 25      # ignore errors smaller than this many pixels (reduces jitter)
SMOOTH = 0.4        # 0 to 1: lower = smoother but slower
# -------------------------------------------------------------------------

PAN_MIN, PAN_MAX = 30, 150          # same limits as serial_servo.ino
TILT_MIN, TILT_MAX = 50, 130


def find_target(frame, lower_hsv, upper_hsv):
    """Return (x, y, radius) of the biggest blob in the color range, or None values."""
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, None, None
    biggest = max(contours, key=cv2.contourArea)
    (x, y), radius = cv2.minEnclosingCircle(biggest)
    if radius < 10:
        return None, None, None
    return int(x), int(y), int(radius)


def clamp(value, low, high):
    return max(low, min(high, value))


ser = serial.Serial(PORT, 115200, timeout=1)
time.sleep(2)                       # the Arduino restarts when the port opens

pan, tilt = 90.0, 90.0
ser.write(f"{int(pan)},{int(tilt)}\n".encode())

cap = cv2.VideoCapture(CAMERA_INDEX)
smooth_x, smooth_y = None, None
delays_ms = []                      # time from frame captured to command sent

while True:
    ok, frame = cap.read()
    t_captured = time.perf_counter()
    if not ok:
        break

    height, width = frame.shape[:2]
    x, y, radius = find_target(frame, LOWER, UPPER)

    if x is not None:
        # smooth the ball position so the servos do not chase noise
        smooth_x = x if smooth_x is None else SMOOTH * x + (1 - SMOOTH) * smooth_x
        smooth_y = y if smooth_y is None else SMOOTH * y + (1 - SMOOTH) * smooth_y

        error_x = smooth_x - width / 2        # pixels the ball is from the image center
        error_y = smooth_y - height / 2

        if abs(error_x) > DEAD_ZONE:
            pan = clamp(pan + PAN_SIGN * GAIN * error_x, PAN_MIN, PAN_MAX)
        if abs(error_y) > DEAD_ZONE:
            tilt = clamp(tilt + TILT_SIGN * GAIN * error_y, TILT_MIN, TILT_MAX)

        ser.write(f"{int(round(pan))},{int(round(tilt))}\n".encode())
        delays_ms.append((time.perf_counter() - t_captured) * 1000)

        cv2.circle(frame, (x, y), radius, (0, 255, 255), 2)
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

    cv2.imshow("Follow (q to quit)", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
ser.close()
cv2.destroyAllWindows()

if delays_ms:
    result = (f"Commands sent: {len(delays_ms)}\n"
              f"Median delay: {statistics.median(delays_ms):.1f} ms")
else:
    result = "The ball was never found."

print(result)
with open(SAVE_PATH, "a") as f:    
	f.write(result + "\n\n")
input("Press Enter to close...")