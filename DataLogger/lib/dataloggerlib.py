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


DEBUG = False


class Button:
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
    def __init__(self, name):
        self.name = name

    def read_sensor(self):
        pass

    def serial_display(self):
        """Print serial info, return number of lines printed 
        for interactive displays"""
        print("Function not yet implemented")
        return 1

    def cpx_neopixel_display(self, pixels):
        pixels[:] = [0x000000] * len(pixels)

    def cpx_neopixel_indicator(self, pixels):
        pixels[:] = [0x000000] * len(pixels)
    

class LightSensor(Sensor):
    def __init__(self):
        self.name = "LIGHT"
        self.light = analogio.AnalogIn(board.A8)
        self.value = 0

    def read_sensor(self):
        self.value = self.light.value

    def serial_display(self):
        print(str(self.value))
        return 1

    def cpx_neopixel_indicator(self,pixels):
        pixels[:] = [0x000000] * len(pixels)
        pixels[1] = 0xFFFFFF

class TempSensor(Sensor):
    def __init__(self):
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
        print("{: .3f} *C\n{: .3f} *F".format(self.celsius,
                                                fahrenheit))
        return 2

    def cpx_neopixel_indicator(self, pixels):
        pixels[:] = [0x000000] * len(pixels)
        pixels[8] = 0xFFFFFF

class AccelSensor(Sensor):
    def __init__(self):
        self.name = "ACCEL"
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
        return 3

    def cpx_neopixel_display(self, pixels):
        """atan2 eqn from figure 7 of
           https://www.digikey.com/en/articles/using-an-accelerometer-for-inclination-sensing"""
        if self.z > .92:
            pixels[:] = [0x000000] * len(pixels)
            return
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
        
    def cpx_neopixel_indicator(self,pixels):
        pixels[:] = [0x000000] * len(pixels)
        pixels[0] = 0xFFFFFF
        pixels[4] = 0xFFFFFF
        pixels[5] = 0xFFFFFF
        pixels[9] = 0xFFFFFF
