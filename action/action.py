import RPi.GPIO as GPIO
from datetime import timedelta
import os

from speaker import speaker
from hue import *

class Action:
    def __init__(self, function, duration, name):
        self.function = function
        self.duration = duration
        self.name = name

    def run(self):
        self.function()

actions = [
    Action(lambda : speaker.set_alarm_volume(0.02), timedelta(minutes=60), 'volume 10'),
    Action(speaker.alarm_start, timedelta(minutes=60), 'music'),
    Action(lambda : speaker.set_alarm_volume(0.03), timedelta(minutes=55), 'volume 15'),
    Action(lambda : speaker.set_alarm_volume(0.05), timedelta(minutes=50), 'volume 20'),
    Action(lambda : hue_on(0, 0, 255), timedelta(minutes=11), 'hue on'),
    Action(lambda : speaker.set_alarm_volume(0.60), timedelta(minutes=11), 'volume 60'),
    Action(speaker.old_alarm_start, timedelta(minutes=10), 'old alarm'),
]

def clean_up():
    speaker.alarm_stop()
    speaker.old_alarm_stop()
    GPIO.cleanup()
