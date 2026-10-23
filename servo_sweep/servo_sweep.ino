// servo_sweep.ino
// Step 1 on the Arduino: slowly sweep each servo to prove the wiring works.
// Pan servo (bottom) signal wire -> pin 9. Tilt servo (top) signal wire -> pin 10.

#include <Servo.h>

Servo pan;
Servo tilt;

void setup() {
  pan.attach(9);
  tilt.attach(10);
  pan.write(90);    // 90 degrees = centered
  tilt.write(90);
  delay(1000);
}

void loop() {
  // Sweep the pan servo from 60 to 120 degrees and back (small range to be safe)
  for (int a = 60; a <= 120; a++) { pan.write(a); delay(15); }
  for (int a = 120; a >= 60; a--) { pan.write(a); delay(15); }

  // Sweep the tilt servo the same way
  for (int a = 60; a <= 120; a++) { tilt.write(a); delay(15); }
  for (int a = 120; a >= 60; a--) { tilt.write(a); delay(15); }
}
