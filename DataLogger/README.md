# Circuit Express Data Logger

This program was written for CircuitPython version 9.2.1

Program to visualize sensor data from the Adafruit circuit playground express using onboard leds and serial output 

The program allows the user to select a sensor using the "A" button (an LED indicator illuminates to show which sensor is selected). Then the "B" button is pressed to start reading the sensor (and a small red LED illuminates to show reading the device is reading). Data is output to either the board LEDS, the serial port, or both. To select a different sensor, reading must be paused by pressing the "B" button again. 

**Current Features**
| Sensor        | Reading | Serial Display | LED Display |
| ------------- | ------- | -------------- | ----------- |
| Temperature   | ✅      | ✅             | ❌          |
| Light         | ✅      | ✅             | ❌          |
| Accelerometer | ✅      | ✅             | ✅          |
| Sound         | ❌      | ❌             | ❌          |

## Build Process
A large portion of the program code is implemented in the dataloggerlib library in the lib directory. This code must be compiled before being loaded onto the microcontroller, otherwise the system will run out of memory when it attempts to compile the code on-board. If no change is made to the dataloggerlib, the existing `dataloggerlib.mpy` file can be used. If changes are made, then the library will need to be recompiled.

To compile the code download [mpy-cross](https://learn.adafruit.com/welcome-to-circuitpython/frequently-asked-questions#faq-3105290) and follow instructions to run it against the `dataloggerlib.py` file to generate a new `dataloggerlib.mpy` file.

## Running
Copy _only_ the `dataloggerlib.mpy` file into the microcontroller `lib` directory, then copy the `code.py` to the top level directory of the microcontroller, and ensure there are no other files named `code.txt`, `main.txt`, or `main.py` in the top level directory.

> [!IMPORTANT]  
> If the `.py` file is copied to the lib directory it will override the `.mpy` file
> this will likely result in a `MemoryError`

For macOS/linux/WSL the `circex-py-build` script in the `build` directory can be used to compile the libraries, copy resulting code to the microcontroller and open the serial monitor.
