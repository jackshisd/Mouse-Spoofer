# Mouse Spoofer – Human-like USB Mouse Activity Emulator
## Overview
This project is a USB mouse spoofer designed for a friend whose job tracked mouse movement to verify work hours. The device emulates realistic human-like mouse activity, preventing the computer from going idle and maintaining the appearance of activity.

Built using a Raspberry Pi Pico (2020 model) and written in Python (via CircuitPython or MicroPython), it features plug-and-play functionality and requires no software setup on the host machine.

## Features
- USB HID mouse emulation via Pi Pico

- Randomized, lifelike mouse movements to avoid detection

- Single-button control to toggle on/off

- LED indicator shows when spoofing is active

- Plug-and-play — no drivers or configuration needed

- Works on Windows, macOS, and Linux

## Hardware Setup
### Component	Connection Details
- Button	One leg to GND, other to GPIO 12
- LED + Resistor	GPIO 21 → 220Ω resistor → LED → GND

*Note: Internal pull-up resistor is used for the button pin.*

## Requirements
- Raspberry Pi Pico (2020 model)

- MicroPython or CircuitPython firmware installed

- USB cable for connection to computer

- 1x button

- 1x LED

- 1x 220Ω resistor

- Soldering or breadboard setup

## How It Works
When plugged in, the Pi Pico identifies as a USB mouse

Pressing the button starts or stops the mouse spoofing script

When active, the script randomly moves the cursor at intervals that mimic human behavior

The LED turns on to indicate active spoofing

Ideal for preventing screensavers or inactivity detection

## Usage
Flash MicroPython or CircuitPython onto your Pico

Copy the main.py script to the Pico’s filesystem

Plug the Pico into a computer

Press the button to start spoofing; LED will turn on

Press again to stop

## Disclaimer
This project was created for educational purposes only. Using tools like this to circumvent employer policies may violate workplace agreements or local laws. Use responsibly.

# 🧑‍🔬 Author
Jack Shi
🛠️ Hardware tinkerer • 📫 jackmshi@ucla.edu
