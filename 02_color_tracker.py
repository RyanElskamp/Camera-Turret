# 02_color_tracker.py
# Step 2: find a brightly colored ball in the webcam feed and mark its center.
# Use the sliders to tune the color. Press q to quit; the final values are printed.

import cv2
import numpy as np


def find_target(frame, lower_hsv, upper_hsv):
    """Return (x, y, radius, mask) for the biggest blob in the color range.
    x, y, radius are None if nothing is found."""
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)          # smooth out noise
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)          # hue is easier to match than BGR
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)           # white where the color matches
    mask = cv2.erode(mask, None, iterations=2)              # remove small specks
    mask = cv2.dilate(mask, None, iterations=2)             # grow the blob back

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, None, None, mask

    biggest = max(contours, key=cv2.contourArea)
    (x, y), radius = cv2.minEnclosingCircle(biggest)
    if radius < 10:                                         # too small to be the ball
        return None, None, None, mask
    return int(x), int(y), int(radius), mask


def nothing(_):
    pass


def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)                # use 1 for the USB webcam if needed
    if not cap.isOpened():
        print("Could not open the camera.")
        return

    # Sliders. Start values are for a bright green ball; change them for your ball.
    cv2.namedWindow("Controls")
    cv2.createTrackbar("H low", "Controls", 35, 179, nothing)
    cv2.createTrackbar("H high", "Controls", 85, 179, nothing)
    cv2.createTrackbar("S low", "Controls", 100, 255, nothing)
    cv2.createTrackbar("V low", "Controls", 100, 255, nothing)

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        h_low = cv2.getTrackbarPos("H low", "Controls")
        h_high = cv2.getTrackbarPos("H high", "Controls")
        s_low = cv2.getTrackbarPos("S low", "Controls")
        v_low = cv2.getTrackbarPos("V low", "Controls")
        lower = np.array([h_low, s_low, v_low])
        upper = np.array([h_high, 255, 255])

        x, y, radius, mask = find_target(frame, lower, upper)

        if x is not None:
            cv2.circle(frame, (x, y), radius, (0, 255, 255), 2)   # outline the ball
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)          # dot at its center

        cv2.imshow("Tracker (press q to quit)", frame)
        cv2.imshow("Mask (white = matched color)", mask)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Final values: lower =", [h_low, s_low, v_low], "upper =", [h_high, 255, 255])
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
