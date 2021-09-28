import RPi.GPIO as GPIO
from time import sleep

pin = 40
duration = 0.4
delay = 0.2
frequency = 700
start_val = 50
reps = 10

GPIO.setup(pin, GPIO.OUT)

p = GPIO.PWM(pin, 50)

def alarm_until(should_stop):
    i = 0
    while not should_stop(i):
        i += 1
        p.start(start_val)
        p.ChangeFrequency(frequency)
        sleep(duration)
        p.stop()
        sleep(delay)
