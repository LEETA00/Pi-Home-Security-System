# # Pi Home Security System

A motion-triggered security camera built on a Raspberry Pi 4. An HC-SR04 ultrasonic sensor watches a doorway or room. When something comes within the set distance, the Pi camera captures a photo, a buzzer sounds, and the event is logged to CSV. Built together with a friend.

> This repository is a clean rewrite of the project, published as a reference implementation. Check pin numbers against your own wiring.

## Hardware
Raspberry Pi 4, Pi Camera Module (ribbon cable), HC-SR04 ultrasonic sensor, active buzzer, breadboard, jumper wires, 1k and 2k resistors.

| Part | Pi pin |
|---|---|
| HC-SR04 VCC / GND | 5V / GND |
| HC-SR04 TRIG | GPIO 23 |
| HC-SR04 ECHO | GPIO 24, through a voltage divider |
| Buzzer + | GPIO 17 |

The HC-SR04 ECHO pin outputs 5V and Pi GPIO is 3.3V only. Use a divider: ECHO to a 1k resistor to GPIO 24, and GPIO 24 through a 2k resistor to GND.

## Setup

    sudo apt install -y python3-picamera2 python3-gpiozero
    python3 security.py

Photos are saved to `captures/` and events to `events.csv`. Tune `THRESHOLD_M` and `COOLDOWN_S` at the top of `security.py`.

## Roadmap
Email or Telegram alerts, a PIR sensor for wider coverage, video clips instead of stills, a web viewer for captures.