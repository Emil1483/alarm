import RPi.GPIO as GPIO

pin = 16

GPIO.setup(pin, GPIO.IN)

def sensor():
    return GPIO.input(pin)
