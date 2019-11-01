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
# cyprus.setup_servo(2)
# cyprus.set_servo_position(2, 0.5)

cyprus.set_servo_position(1, 0)
sleep(1)
cyprus.set_servo_position(1, 1)

# for i in range(1, 41):
#     number = 0.5 + i/80.0
#     cyprus.set_servo_position(2, number)
#     print(number)
#     sleep(0.5)

# sleep(1)
# cyprus.set_servo_position(2, 0.5)

limit_pressed = (cyprus.read_gpio() & 0b0001) == 0
counter = 0
'''
while counter != 50:
    if not limit_pressed and (cyprus.read_gpio() & 0b0001) == 0:    # switch just got pressed
        sleep(0.05)                                                 # debounce
        if cyprus.read_gpio() & 0b0001 == 0:
            limit_pressed = True
            cyprus.set_servo_position(1, 0)                         # 0 deg if pressed
    elif limit_pressed and (cyprus.read_gpio() & 0b0001) == 1:      # switch just got unpressed
        sleep(0.05)                                                 # debounce
        if cyprus.read_gpio() & 0b0001 == 1:
            limit_pressed = False
            cyprus.set_servo_position(1, 1)                         # 180 deg if unpressed
    sleep(0.1)
    counter += 1
'''
proximate = (cyprus.read_gpio() & 0b0001) == 0

print("starting to check; " + str(proximate))

for i in range(1000):
    print(str(proximate))
    print(cyprus.read_gpio() & 0b0001)
    if not proximate and (cyprus.read_gpio() & 0b0001) == 0:        # proximity detected
        sleep(0.1)
        if cyprus.read_gpio() & 0b0001 == 0:
            proximate = True
            cyprus.set_pwm_values(2, period_value=100000, compare_value=100000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
    elif proximate and ((cyprus.read_gpio() & 0b0001) == 1):
        sleep(0.1)
        if cyprus.read_gpio() & 0b0001 == 1:
            proximate = False
            cyprus.set_pwm_values(2, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
    sleep(0.05)

cyprus.close()
