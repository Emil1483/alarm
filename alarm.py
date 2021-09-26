import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

from speaker import *
from sensor import *

curr = sensor()
alarm_until(lambda : sensor() != curr)

GPIO.cleanup()
