import board
import countio
import adafruit_thermistor
import digitalio
import analogio
import time
import adafruit_lis3dh
import busio

from digitalio import DigitalInOut, Direction, Pull

# Dave was here
DEBUG = False

def init_thermistor():
    """Return a thermistor object that can be queried for the temperature"""
    pin = board.TEMPERATURE
    resistor = 10000
    resistance = 10000
    nominal_temp = 25
    b_coefficient = 3950

    thermistor = adafruit_thermistor.Thermistor(
        pin, resistor, resistance, nominal_temp, b_coefficient
    )

    return thermistor


def init_accel():
    """Return an accelerometer object that can be queried for X/Y/Z accelerations"""
    i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
    lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)

    return lis3dh


class button:
    def __init__(self, in_pin):
        self.button_counter = countio.Counter(in_pin, edge=countio.Edge.RISE, pull=Pull.DOWN)
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


def rwd_lines(lines):
    # TODO: Support variable number of output lines
    if not DEBUG:
        print("\033[2K\033[F"*(lines+1))

#---------------------------------------------------------------
# Program starts here
if __name__ == "__main__":
    MODE_LIST = ["TEMP", "GYRO", "SOUND", "LIGHT", "MICROPHONE"]
    mode_current=0
    record_state = False

    a_button = button(board.D4)
    b_button = button(board.D5)

    light = analogio.AnalogIn(board.A8)
    thermistor = init_thermistor()
    accel = init_accel()

    print("\033[?25l")
    print("Mode: " + MODE_LIST[mode_current] + "\n\n\n")
    while True:
        if (a_button.pressed()):
            mode_current = (mode_current + 1) % len(MODE_LIST)
            rwd_lines(4)
            print("Mode: " + MODE_LIST[mode_current] + "\n\n\n")

        if (b_button.pressed()):
            record_state = ~record_state

        if record_state:
            rwd_lines(3)

            if MODE_LIST[mode_current] == "TEMP":
                celsius = thermistor.temperature
                fahrenheit = (celsius * 9 / 5) + 32
                print("{: .3f} *C\n{: .3f} *F\n"
                        .format(celsius, fahrenheit))

            elif MODE_LIST[mode_current] == "LIGHT":
                print(str(light.value) + "\n\n")

            elif MODE_LIST[mode_current] == "GYRO":
                x, y, z = [value / adafruit_lis3dh.STANDARD_GRAVITY
                    for value in accel.acceleration]
                print("x = {: .3f} G\ny = {: .3f} G\nz = {: .3f} G"
                        .format(x,y,z))

            else:
                print("Function not yet implemented\n\n")

        else:
            rwd_lines(3)
            print("Press B to start recording\n\n")
        time.sleep(0.1)
