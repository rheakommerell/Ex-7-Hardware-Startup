"""
@file selfupdatinglabeldecimalformat.py This file is responsible for holding the SelfUpdatingLabel Class
"""

from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import ObjectProperty


class SelfUpdatingLabel(Label):
    """
    Class to update a label's text in a given frequency
    """

    def __init__(self, **kwargs):
        """Super the Label constructor to ensure the Label functions properly"""
        super(SelfUpdatingLabel, self).__init__(**kwargs)

        """Set update_property and update_frequency to be appropriate kivy properties"""
        self.update_property = ObjectProperty(defaultvalue=None)
        self.update_property_parameters = ObjectProperty(defaultvalue=None)
        self.update_frequency = ObjectProperty(defaultvalue=0.25)

        """Call update_text with the user given update_frequency"""
        Clock.schedule_interval(lambda args: self.update_text(), 0.1)

    def update_text(self) -> None:
        """
        Update the text with the given update_property at the given update_frequency.
        To update text based off a given function set update_property: object.function with no parenthesis
        If the function you are calling includes parameters specify them in update_property_parameters
        :return: None
        """
        if self.update_property is None:
            return
        elif callable(self.update_property):  # if the update_property is a method to call
            if self.update_property_parameters is not None:  # call with given parameters
                self.text = str(self.update_property(self.update_property_parameters))
            else:
                self.text = str(self.update_property())
        else:  # Set to whatever was given
            self.text = str(self.update_property)
