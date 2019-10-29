import spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus
spi = spidev.SpiDev()

cyprus.initialize()  # initialize the RPiMIB and establish communication
cyprus.setup_servo(1)
cyprus.setup_servo(2)
cyprus.set_servo_position(2, 0.5)

cyprus.set_servo_position(1, 0)
sleep(1)
cyprus.set_servo_position(1, 1)

limit_pressed = False

while True:
    print("lp " + str(limit_pressed))
    print("actual " + str(cyprus.read_gpio() & 0b0001))
    if not limit_pressed & (cyprus.read_gpio() & 0b0001) == 1:      # switch just got pressed
        sleep(0.05)                                                 # debounce
        if cyprus.read_gpio() & 0b0001:
            limit_pressed = True
            cyprus.set_servo_position(1, 0)                         # 0 deg if pressed
    elif limit_pressed & (cyprus.read_gpio() & 0b0001) == 0:        # switch just got unpressed
        print("it work")
        sleep(0.05)                                                 # debounce
        if not (cyprus.read_gpio() & 0b0001):
            limit_pressed = False
            cyprus.set_servo_position(1, 1)                         # 180 deg if unpressed

