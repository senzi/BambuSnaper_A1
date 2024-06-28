This script configures a microcontroller to act as a USB HID (Human Interface Device) device, capable of controlling consumer control codes (like volume) and simulating mouse movements. The script also uses a GPIO pin to detect a button press, which triggers a specific action (e.g., simulating a camera shutter by sending a volume decrement command).

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Code Overview](#code-overview)
- [License](#license)

## Introduction

This project demonstrates how to use a microcontroller to interact with a computer via USB HID. The script continuously monitors a button connected to a GPIO pin and simulates mouse movements every 15 seconds to prevent the computer from going to sleep. Additionally, pressing the button triggers a simulated camera shutter by sending a volume decrement command.

## Features

- Simulate mouse movements every 15 seconds to prevent sleep mode.
- Use a button connected to a GPIO pin to send a consumer control code (volume decrement).
- Configurable GPIO pin for button input.
- Debounce logic for button presses.

## Hardware Requirements

- A microcontroller with USB HID support (e.g., Raspberry Pi Pico, Adafruit ItsyBitsy, etc.).
- A button connected to a GPIO pin (configured with an internal pull-up resistor).

## Software Requirements

- CircuitPython or a similar Python environment for microcontrollers.
- Libraries:
  - `adafruit_hid`
  - `digitalio`
  - `board`
  - `time`

## Setup

1. **Install CircuitPython**: Follow the instructions to install CircuitPython on your microcontroller board from the [official CircuitPython website](https://circuitpython.org/).

2. **Install Required Libraries**: Use the `circup` utility to install the necessary libraries:
    ```bash
    circup install adafruit_hid digitalio board
    ```

3. **Connect the Button**: 
    - Connect one side of the button to the GPIO pin `GP10` on the board.
    - Connect the other side of the button to the ground (GND).

4. **Upload the Script**: Copy the provided script to your microcontroller's file system, typically as `code.py`.

## Usage

Once the script is uploaded and the board is powered on, it will:
- Move the mouse cursor slightly every 15 seconds to prevent the computer from going to sleep.
- Detect button presses on the configured GPIO pin (`GP10`) and send a volume decrement command each time the button is pressed.

## Code Overview

The script performs the following tasks:
1. **Initialize HID Devices**:
    ```python
    cc = ConsumerControl(usb_hid.devices)
    mouse = Mouse(usb_hid.devices)
    ```

2. **Set Up Button Input**:
    ```python
    button_pin = digitalio.DigitalInOut(board.GP10)
    button_pin.direction = digitalio.Direction.INPUT
    button_pin.pull = digitalio.Pull.UP
    ```

3. **Define the Action Function**:
    ```python
    def take_photo():
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
    ```

4. **Main Loop**:
    - Sleep for a short period to reduce CPU usage.
    - Check if 15 seconds have passed to move the mouse cursor.
    - Check if the button is pressed to trigger the camera shutter action.
    - Implement debouncing by waiting for the button to be released.

    ```python
    while True:
        time.sleep(0.1)  # Every 0.1 second

        if time.time() - last_activity_time >= 15:
            mouse.move(x=10, y=0)
            last_activity_time = time.time()

        if not button_pin.value:
            take_photo()
            while not button_pin.value:
                time.sleep(0.01)
    ```

## License

This project is open source and available under the MIT License. See the LICENSE file for more information.