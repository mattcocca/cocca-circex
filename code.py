import board
import countio
import adafruit_thermistor
import digitalio
import time

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
            if mode_current == 0:
                celsius = thermistor.temperature
                fahrenheit = (celsius * 9 / 5) + 32
                print("\033[K== Temperature ==\n\033[K{} *C\n\033[K{} *F".format(celsius, fahrenheit))
            else:
                print("\033[KFunction not yet implemented\n\033[K\n\033[K")
        else:
            print("\033[KPress B to start recording\n\033[K\n\033[K")
        print("\033[F\033[F\033[F\033[F") # TODO: Support variable number of output lines