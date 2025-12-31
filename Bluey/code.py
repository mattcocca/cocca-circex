# SPDX-FileCopyrightText: 2017 John Edgar Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Circuit Playground NeoPixel
import time
import board
from rainbowio import colorwheel
import neopixel

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.3, auto_write=False)

# choose which demos to play
# 1 means play, 0 means don't!
color_chase_demo = 0
blue_chase_demo = 0
flash_demo = 0
blue_flash_demo = 1
rainbow_demo = 0
rainbow_cycle_demo = 0


def color_chase(color, wait):
    for i in range(10):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)

def blue_chase(color, wait):
    for i in range(10):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(10):
            rc_index = (i * 256 // 10) + j * 5
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)


def rainbow(wait):
    for j in range(255):
        for i in range(len(pixels)):
            idx = int(i + j)
            pixels[i] = colorwheel(idx & 255)
        pixels.show()
        time.sleep(wait)


RED = (255, 0, 0)
YELLOW = (180, 180, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (150, 0, 150)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)
BLUE0 = (0, 0, 255)
BLUE1 = (0, 15, 240)
BLUE2 = (0, 30, 225)
BLUE3 = (0, 45, 210)
BLUE4 = (0, 60, 195)
BLUE5 = (0, 75, 180)
BLUE6 = (0, 90, 165)
BLUE7 = (0, 105, 150)
BLUE8 = (0, 120, 135)
BLUE9 = (0, 135, 120)

while True:
    if color_chase_demo:
        color_chase(RED, 0.1)  # Increase the number to slow down the color chase
        color_chase(YELLOW, 0.1)
        color_chase(GREEN, 0.1)
        color_chase(CYAN, 0.1)
        color_chase(BLUE, 0.1)
        color_chase(PURPLE, 0.1)
        color_chase(OFF, 0.1)

    if flash_demo:
        pixels.fill(RED)
        pixels.show()
        # Increase or decrease to change the speed of the solid color change.
        time.sleep(1)
        pixels.fill(GREEN)
        pixels.show()
        time.sleep(1)
        pixels.fill(BLUE)
        pixels.show()
        time.sleep(1)
        pixels.fill(WHITE)
        pixels.show()
        time.sleep(1)

    if blue_chase_demo:
        blue_chase(BLUE0, 0.1)  # Increase the number to slow down the color chase
        blue_chase(BLUE1, 0.1)
        blue_chase(BLUE2, 0.1)
        blue_chase(BLUE3, 0.1)
        blue_chase(BLUE4, 0.1)
        blue_chase(BLUE5, 0.1)
        blue_chase(BLUE6, 0.1)
        blue_chase(BLUE7, 0.1)
        blue_chase(BLUE8, 0.1)
        blue_chase(BLUE9, 0.1)

    if blue_flash_demo:
        pixels.fill(BLUE0)
        pixels.show()
        # Increase or decrease to change the speed of the solid color change.
        time.sleep(1)
        pixels.fill(BLUE1)
        pixels.show()
        time.sleep(1)
        pixels.fill(BLUE2)
        pixels.show()
        time.sleep(1)
        pixels.fill(BLUE3)
        pixels.show()
        time.sleep(1)
        pixels.fill(BLUE4)
        pixels.show()
        time.sleep(1)
        pixels.fill(BLUE5)
        pixels.show()
        time.sleep(1)
        pixels.fill(BLUE6)
        pixels.show()
        time.sleep(1)
        pixels.fill(BLUE7)
        pixels.show()
        time.sleep(1)
        pixels.fill(BLUE8)
        pixels.show()
        time.sleep(1)
        pixels.fill(BLUE9)
        pixels.show()
        time.sleep(1)

    if rainbow_cycle_demo:
        rainbow_cycle(0.05)  # Increase the number to slow down the rainbow.

    if rainbow_demo:
        rainbow(0.05)  # Increase the number to slow down the rainbow.
