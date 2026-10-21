# Camera-Turret# \# camera-turret

# 

# A two-axis camera tracking turret. An Arduino Uno drives two servos on a pan-tilt bracket, and Python with OpenCV finds a colored ball in a webcam feed and tells the servos where to point.

# 

# \*\*Status:\*\* in progress (started Oct 2026)

# 

# \## Goal

# Track a moving target and measure the delay from camera frame to servo command.

# 

# \## Hardware

# \- Arduino Uno

# \- Pan-tilt bracket with two micro servos

# \- USB webcam (Logitech C270)

# \- Separate 5 V supply for the servos

# 

# \## Software

# \- Python 3 with OpenCV (`pip install opencv-python numpy`)

# \- Arduino IDE

# 

# \## Progress

# \- \[ ] Webcam feed in OpenCV (`01\\\_webcam\\\_feed.py`)

# \- \[ ] Color detection with adjustable sliders (`02\\\_color\\\_tracker.py`)

# \- \[ ] Servos assembled and wired

# \- \[ ] Arduino sketch to move the servos

# \- \[ ] Python sends angles to the Arduino

# \- \[ ] Turret follows the target

# \- \[ ] Measure the response time

# 

# \## How to run

# ```

# python 01\_webcam\_feed.py

# python 02\_color\_tracker.py

# ```

# Press `q` to quit.

# 

