import RPi.GPIO as GPIO
from datetime import timedelta

from speaker import *

class Action:
    def __init__(self, function, duration):
        self.function = function
        self.duration = duration

    def run(self):
        self.function()

actions = [
    Action(alarm_start, timedelta(minutes=50)),
    Action(old_alarm_start, timedelta(minutes=40))
]

def clean_up():
    alarm_stop()
    old_alarm_stop()
    GPIO.cleanup()
