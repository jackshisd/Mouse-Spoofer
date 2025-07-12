import time
import usb_hid
import random
import board
import digitalio
from adafruit_hid.mouse import Mouse
import digitalio
import board

# -----------------------
# LED Setup
# -----------------------

led_pin = digitalio.DigitalInOut(board.GP21)
led_pin.direction = digitalio.Direction.OUTPUT
led_pin.value = False   # start off
# -----------------------
# Kill Switch (Toggle) Setup
# -----------------------

toggle_pin = digitalio.DigitalInOut(board.GP12)
toggle_pin.direction = digitalio.Direction.INPUT
toggle_pin.pull = digitalio.Pull.UP

# -----------------------
# Mouse Setup
# -----------------------

mouse = Mouse(usb_hid.devices)

# -----------------------
# Smooth Movement Config
# -----------------------

TARGET_MIN_OFFSET = 80     # min distance for a target movement
TARGET_MAX_OFFSET = 300    # max distance for a target movement
STEP_MIN = 10              # minimum pixels per step
STEP_MAX = 30              # maximum pixels per step
STEP_DELAY_MIN = 0.03      # delay between small steps (seconds)
STEP_DELAY_MAX = 0.08

PAUSE_MIN = 0.5            # pause after reaching target
PAUSE_MAX = 2.5

# -----------------------
# Debounce Config
# -----------------------

DEBOUNCE_TIME = 0.2        # seconds

print("Smooth mouse jiggler running. Press GP12 to toggle on/off.")

# Initial state
jiggler_active = True

# Track previous button state
prev_button_state = toggle_pin.value
last_toggle_time = time.monotonic()

# Start with no target
current_dx = 0
current_dy = 0
remaining_dx = 0
remaining_dy = 0

# For time-based stepping
next_move_time = time.monotonic()
pause_until = None

while True:
    now = time.monotonic()

    led_pin.value = jiggler_active

    # -----------------------
    # Check the button
    # -----------------------

    current_button_state = toggle_pin.value

    if (
        prev_button_state and
        not current_button_state and
        (now - last_toggle_time) > DEBOUNCE_TIME
    ):
        jiggler_active = not jiggler_active
        last_toggle_time = now

        if jiggler_active:
            print("Jiggler turned ON.")
            # Reset everything fresh
            remaining_dx = 0
            remaining_dy = 0
            pause_until = None
        else:
            print("Jiggler turned OFF.")
            remaining_dx = 0
            remaining_dy = 0
            pause_until = None

    prev_button_state = current_button_state

    if not jiggler_active:
        time.sleep(0.01)
        continue

    # -----------------------
    # Handle pause after reaching a target
    # -----------------------

    if pause_until is not None:
        if now >= pause_until:
            pause_until = None
        else:
            time.sleep(0.001)
            continue

    # -----------------------
    # Pick new target if needed
    # -----------------------

    if remaining_dx == 0 and remaining_dy == 0 and pause_until is None:
        current_dx = random.randint(-TARGET_MAX_OFFSET, TARGET_MAX_OFFSET)
        current_dy = random.randint(-TARGET_MAX_OFFSET, TARGET_MAX_OFFSET)

        if abs(current_dx) < TARGET_MIN_OFFSET:
            current_dx = TARGET_MIN_OFFSET * (1 if current_dx >= 0 else -1)
        if abs(current_dy) < TARGET_MIN_OFFSET:
            current_dy = TARGET_MIN_OFFSET * (1 if current_dy >= 0 else -1)

        remaining_dx = current_dx
        remaining_dy = current_dy

        print(f"New target: ({current_dx}, {current_dy})")

    # -----------------------
    # Move one step if delay passed
    # -----------------------

    if now >= next_move_time and (remaining_dx != 0 or remaining_dy != 0):
        # Choose dynamic step size for smoother feel
        step_size = random.randint(STEP_MIN, STEP_MAX)

        step_dx = step_size if remaining_dx > 0 else (-step_size if remaining_dx < 0 else 0)
        step_dy = step_size if remaining_dy > 0 else (-step_size if remaining_dy < 0 else 0)

        if abs(remaining_dx) < abs(step_dx):
            step_dx = remaining_dx
        if abs(remaining_dy) < abs(step_dy):
            step_dy = remaining_dy

        if step_dx != 0 or step_dy != 0:
            mouse.move(x=step_dx, y=step_dy)
            remaining_dx -= step_dx
            remaining_dy -= step_dy
            print(f"Moved by ({step_dx}, {step_dy})")

        # Randomize delay for natural pacing
        next_move_time = now + random.uniform(STEP_DELAY_MIN, STEP_DELAY_MAX)

        if remaining_dx == 0 and remaining_dy == 0:
            pause_duration = random.uniform(PAUSE_MIN, PAUSE_MAX)
            pause_until = now + pause_duration
            print(f"Reached target. Pausing for {pause_duration:.2f} sec.")

    time.sleep(0.001)
