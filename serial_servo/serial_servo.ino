// serial_servo.ino
// Move the servos from commands sent over USB.
// Send a line like:  90,90   (pan angle, comma, tilt angle, then Enter)
// In the Arduino Serial Monitor: set the baud to 115200 and line ending to "Newline".

#include <Servo.h>

Servo pan;
Servo tilt;

// Safe limits so the bracket never hits its stops. Widen them slowly if you want.
const int PAN_MIN = 30;
const int PAN_MAX = 150;
const int TILT_MIN = 50;
const int TILT_MAX = 130;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(50);       // do not wait long for a line to finish
  pan.attach(9);
  tilt.attach(10);
  pan.write(90);
  tilt.write(90);
}

void loop() {
  if (Serial.available() > 0) {
    String line = Serial.readStringUntil('\n');
    int comma = line.indexOf(',');
    if (comma > 0) {
      int p = line.substring(0, comma).toInt();
      int t = line.substring(comma + 1).toInt();
      pan.write(constrain(p, PAN_MIN, PAN_MAX));
      tilt.write(constrain(t, TILT_MIN, TILT_MAX));
    }
  }
}
