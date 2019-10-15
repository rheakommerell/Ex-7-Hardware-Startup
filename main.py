import os

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton

import spidev
import os
from threading import Thread
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
spi = spidev.SpiDev()


MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White

s1 = stepper(port=1)
s1.setCurrent(8, 10, 10, 10)
s1.setAccel(0x50)
s1.setDecel(0x100)
s1.setMaxSpeed(525)
s1.setMinSpeed(0)
s1.setMicroSteps(32)
s1.steps_per_unit = 518
s1.setThresholdSpeed(1000)
s1.setOverCurrent(2000)
s1.setStallCurrent(2187.5)
s1.setLowSpeedOpt(False)

class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """
    def start_speed_thread(self):
        Thread(target=self.speed_update).start()

    global need_to_leave
    need_to_leave = False
    global motor_running
    motor_running = False
    global motor_dir
    motor_dir = 0

    def speed_update(self):
        while not need_to_leave:
            if motor_running:
                speed = int(self.ids.slider.value)
                s1.softStop()
                s1.run(motor_dir, speed)
            sleep(.1)

    def switch_dir(self):
        global motor_dir
        if motor_dir == 0:
            motor_dir = 1
        else:
            motor_dir = 0
        if motor_running:
            s1.softStop()
            s1.run(motor_dir, int(self.ids.slider.value))

    def off_on(self):
        global motor_running
        if motor_running:
            s1.softStop()
            motor_running = False
        else:
            s1.run(motor_dir, int(self.ids.slider.value))
            motor_running = True

    def special(self):
        global motor_running
        s1.print_status()
        self.ids.position_label.text = str(s1.get_position_in_units())
        if motor_running:
            motor_running = False
            s1.softStop()
        s1.set_speed(1)
        s1.relative_move(15)
        self.ids.position_label.text = str(s1.get_position_in_units())

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        s1.free_all()
        spi.close()
        GPIO.cleanup()
        global need_to_leave
        need_to_leave = True
        quit()


class AdminScreen(Screen):
    """80, 80))
        anim.start(widg)
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        s1.free_all()
        spi.close()
        GPIO.cleanup()
        quit()
"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
s1.free_all()
spi.close()
GPIO.cleanup()

