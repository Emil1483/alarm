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
    Action(lambda : speaker.set_alarm_volume(0.01), timedelta(minutes=90), 'volume 1'),
    Action(speaker.alarm_start, timedelta(minutes=90), 'music'),
    Action(lambda : speaker.set_alarm_volume(0.02), timedelta(minutes=85), 'volume 2'),
    Action(lambda : speaker.set_alarm_volume(0.03), timedelta(minutes=80), 'volume 3'),
    Action(lambda : speaker.set_alarm_volume(0.40), timedelta(minutes=50), 'volume 40'),
    Action(lambda : hue_on(0, 0, 255), timedelta(minutes=50), 'hue on'),
    Action(lambda : speaker.set_alarm_volume(1.00), timedelta(minutes=45), 'volume 100'),
    Action(speaker.old_alarm_start, timedelta(minutes=40), 'old alarm'),
]

def clean_up():
    speaker.alarm_stop()
    speaker.old_alarm_stop()
    GPIO.cleanup()
