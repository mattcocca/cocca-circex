#DataLogger

import board
import countio
import adafruit_thermistor
import digitalio
import analogio
import time
import adafruit_lis3dh
import busio
import math

from neopixel import NeoPixel
from digitalio import DigitalInOut, Direction, Pull

DEBUG = False

def init_thermistor():
    """Return a thermistor object that can be queried for the 
    temperature"""

    return thermistor


def init_accel():
    """Return an accelerometer object that can be queried for X/Y/Z 
    accelerations"""
    i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
    lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)

    return lis3dh


class button:
    def __init__(self, in_pin):
        self.button_counter = countio.Counter(in_pin, 
                                                edge=countio.Edge.RISE,
                                                pull=Pull.DOWN)
        self.last_pressed_time = 0
        self.last_pressed_count = 0

    def pressed(self):
        pressed = False
        current_time = time.monotonic()
        if self.button_counter.count > self.last_pressed_count:
            if DEBUG:
                print("DEBUG: %0.3f, %0.3f" % (self.last_pressed_time,
                                                 current_time))
            if self.last_pressed_time + .250 < current_time:

                pressed = True
            self.last_pressed_time = current_time
            self.last_pressed_count = self.button_counter.count
        return pressed


class Sensor:
    def __init__(self, name, pixels):
        self.name = name
    def read_sensor(self):
        pass
    def serial_display(self):
        print("Function not yet implemented.\n\n")
    def cpx_neopixel_display(self):
        pixels[:] = [0x000000] * len(pixels)
    

class LightSensor(Sensor):
    def __init__(self, pixels):
        self.name = "LIGHT"
        self.light = analogio.AnalogIn(board.A8)
        self.value = 0
    def read_sensor(self):
        self.value = self.light.value
    def serial_display(self):
        print(str(self.value) + "\n\n")
        

class TempSensor(Sensor):
    def __init__(self, pixels):
        self.name = "TEMP"
        pin = board.TEMPERATURE
        resistor = 10000
        resistance = 10000
        nominal_temp = 25
        b_coefficient = 3950

        self.thermistor = adafruit_thermistor.Thermistor(
            pin, resistor, resistance, nominal_temp, b_coefficient
        )
    def read_sensor(self):
        self.celsius = self.thermistor.temperature
    def serial_display(self):
        fahrenheit = (self.celsius * 9 / 5) + 32
        print("{: .3f} *C\n{: .3f} *F\n".format(self.celsius,
                                                fahrenheit))

class AccelSensor(Sensor):
    def __init__(self, pixels):
        self.name = "ACCEL"
        self.pixels = pixels
        i2c = busio.I2C(board.ACCELEROMETER_SCL,
                        board.ACCELEROMETER_SDA)
        self.lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)
        
    def read_sensor(self):
        self.x, self.y, self.z = [value
                                / adafruit_lis3dh.STANDARD_GRAVITY
                                for value in self.lis3dh.acceleration]

    def serial_display(self):
        print("x = {: .3f} G\ny = {: .3f} G\nz = {: .3f} G".format(
                                                                self.x,
                                                                self.y,
                                                                self.z))

    def cpx_neopixel_display(self):
        """atan2 eqn from figure 7 of
           https://www.digikey.com/en/articles/using-an-accelerometer-for-inclination-sensing"""
        point_dir = (math.atan2(self.x, self.y)-math.pi)*-1.91
        pixels.brightness = round((1-abs(self.z))*.05, 2)+.01
        if 0.5 < point_dir < 5.49:
            point_pxl = round(point_dir-1)
        elif 6.5 < point_dir < 11.49:
            point_pxl = round(point_dir-2)
        else:
            return
        if point_pxl != 0:
            pixels[:point_pxl] = [0x000000] * (point_pxl)
        pixels[point_pxl+1:] = [0x000000] * (len(pixels)-(point_pxl+1))
        pixels[point_pxl] = 0xFFFFFF
        

def rwd_lines(lines):
    # TODO: Support variable number of output lines
    if not DEBUG:
        print("\033[2K\033[F"*(lines+1))


if __name__ == "__main__":
    pixels = NeoPixel(board.NEOPIXEL, 10, brightness=.01)

    MODE_LIST = [
                TempSensor(pixels),
                LightSensor(pixels),
                AccelSensor(pixels),
                Sensor("SOUND", pixels)
                ]

    mode_current=0
    record_state = False
    
    a_button = button(board.D4)
    b_button = button(board.D5)

    print("\033[?25l")
    print("Mode: " + MODE_LIST[mode_current].name + "\n\n\n")
    while True:
        if (a_button.pressed()): 
            mode_current = (mode_current + 1) % len(MODE_LIST)
            rwd_lines(4)
            print("Mode: " + MODE_LIST[mode_current].name + "\n\n\n")

        if (b_button.pressed()):
            record_state = ~record_state

        if record_state:
            rwd_lines(3)
        
            MODE_LIST[mode_current].read_sensor()
            MODE_LIST[mode_current].serial_display()
            MODE_LIST[mode_current].cpx_neopixel_display()
        else:
            rwd_lines(3)
            pixels[:] = [0x000000] * len(pixels)
            print("Press B to start recording\n\n")
        time.sleep(0.1)