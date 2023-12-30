import board
import countio
import adafruit_thermistor
import digitalio
import analogio
import time
import adafruit_lis3dh
import busio

from digitalio import DigitalInOut, Direction, Pull


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


if __name__ == "__main__":
    led = DigitalInOut(board.LED)
    led.direction = digitalio.Direction.OUTPUT
    i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
    lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)
    light = analogio.AnalogIn(board.A8)
    thermistor = init_thermistor()
    MODE_LIST = ["TEMP", "GYRO", "SOUND", "LIGHT"]
    mode_current=0
    mode_counter = countio.Counter(board.D4, edge=countio.Edge.RISE, pull=Pull.DOWN)
    record_state=0
    record_counter = countio.Counter(board.D5, edge=countio.Edge.RISE, pull=Pull.DOWN)
    record_state = False
    print("\033[?25l")
    print("Mode: " + MODE_LIST[mode_current])
    while True:
        if (mode_counter.count % len(MODE_LIST)) != mode_current: # TODO: Debounce better (maybe based on time since last change)
            mode_current = mode_counter.count % len(MODE_LIST)
            print("\033[F\033[KMode: " + MODE_LIST[mode_current])
        if record_counter.count%2 != 0:
            if MODE_LIST[mode_current] == "TEMP":
                celsius = thermistor.temperature
                fahrenheit = (celsius * 9 / 5) + 32
                print("\033[K{} *C\n\033[K{} *F".format(celsius, fahrenheit))
            elif MODE_LIST[mode_current] == "LIGHT":
                print("\033[K" + str(light.value) + "\n\033[K")
            elif MODE_LIST[mode_current] == "GYRO":
                x, y, z = [value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration]
                print("\033[Kx = %0.3f G, y = %0.3f G, z = %0.3f G\n\033[K" % (x, y, z))
            else:
                print("\033[KFunction not yet implemented\n\033[K")
        else:
            print("\033[KPress B to start recording\n\033[K")
        print("\033[F\033[F\033[F") # TODO: Support variable number of output lines
