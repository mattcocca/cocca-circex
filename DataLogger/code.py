import board
import countio
import adafruit_thermistor
import analogio
import time
import adafruit_lis3dh
import busio
import math

from neopixel import NeoPixel
from digitalio import DigitalInOut, Direction, Pull

from dataloggerlib import *

def rwd_lines(lines):
    if not DEBUG:
        print("\033[F\033[K\n" + "\033[2K\033[F"*(lines),end="")


if __name__ == "__main__":
    pixels = NeoPixel(board.NEOPIXEL, 10, brightness=.01)

    MODE_LIST = [
                TempSensor(),
                LightSensor(),
                AccelSensor(),
                Sensor("SOUND")
                ]

    mode_current = 0
    record_state = False
    last_disp = 0
    sense_outlines = 0
    
    a_button = Button(board.D4)
    b_button = Button(board.D5)
    record_led = DigitalInOut(board.LED)
    record_led.switch_to_output()

    print("\033[?25l", end="")
    print("\nMode: " + MODE_LIST[mode_current].name + "\n\n")
    while True:
        disp_cycle = False
        current_time =  time.monotonic()
        if last_disp + 0.1 < current_time:
            disp_cycle = True
            last_disp = current_time
        if (a_button.pressed()):
            if not record_state:
                mode_current = (mode_current + 1) % len(MODE_LIST)
                rwd_lines(sense_outlines + 4)
                print("\nMode: " + MODE_LIST[mode_current].name + "\n\n"
                        + "\n"*sense_outlines)
                pixels.brightness = 0.01
                MODE_LIST[mode_current].cpx_neopixel_indicator(pixels)

        if (b_button.pressed()):
            record_state = ~record_state
            record_led.value = record_state
        if record_state:
            MODE_LIST[mode_current].read_sensor()
            current_time =  time.monotonic()
            if disp_cycle:
                rwd_lines(sense_outlines)
                sense_outlines = MODE_LIST[mode_current].serial_display()
                MODE_LIST[mode_current].cpx_neopixel_display(pixels)
        else:
            MODE_LIST[mode_current].cpx_neopixel_indicator(pixels)
            if disp_cycle:
                rwd_lines(sense_outlines)
                print("Press B to start recording")
                sense_outlines = 1
