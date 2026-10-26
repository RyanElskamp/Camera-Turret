# Camera Tracking Turret

A two-axis pan-tilt turret that follows a blue ball. A Logitech C270 webcam feeds
a Python/OpenCV script that finds the ball by HSV color thresholding and sends
pan and tilt angles over USB serial (115200 baud) to an Arduino Uno, which drives
two servos from a separate 5 V supply with a shared ground. Smoothing and a dead
zone reduce servo jitter.

Result: median software processing delay of 1.6 ms (frame capture to servo
command) over 406 frames. This measures processing time only, not camera
latency or servo travel time.

Files: 01_webcam_feed.py, 02_color_tracker.py, 03_keyboard_control.py,
04_follow.py, and the Arduino sketches in servo_sweep and serial_servo.
