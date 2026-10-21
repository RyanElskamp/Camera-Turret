# 01_webcam_feed.py
# Step 1: show the webcam feed in a window. Press q to quit.

import cv2

# 0 is usually the laptop camera. If you plug in the USB webcam and the
# wrong camera shows up, try 1 or 2 instead.
# cv2.CAP_DSHOW makes the camera start faster on Windows.
CAMERA_INDEX = 0
cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Could not open the camera. Try a different CAMERA_INDEX.")
    raise SystemExit

while True:
    ok, frame = cap.read()      # grab one picture from the camera
    if not ok:
        print("Could not read a frame.")
        break

    cv2.imshow("Webcam (press q to quit)", frame)

    # wait 1 ms for a key press; quit if it was q
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
