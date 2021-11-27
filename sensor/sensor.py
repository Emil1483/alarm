import RPi.GPIO as GPIO
from time import sleep

door_pin = 16
button_pin = 36
button_power_pin = 35
motion_pin = 8

GPIO.setmode(GPIO.BOARD)

GPIO.setup(door_pin, GPIO.IN)
GPIO.setup(button_pin, GPIO.IN)
GPIO.setup(button_power_pin, GPIO.OUT)
GPIO.setup(motion_pin, GPIO.IN)

def door_sensor():
    return GPIO.input(door_pin)

def button_sensor():
    return 1 - GPIO.input(button_pin)

def motion_sensor():
    return GPIO.input(motion_pin)

button_is_on = False
def button_set_on(on):
    global button_is_on
    button_is_on = on
    GPIO.output(button_power_pin, on)

def button_toggle_on():
    button_set_on(0 if button_is_on else 1)

def update(name, curr, sensor):
    if curr != sensor:
        print(f'{name}: {curr} --> {sensor}')

    return sensor

if __name__ == '__main__':
    curr_door = door_sensor()
    curr_button = button_sensor()
    curr_motion = motion_sensor()
    while True:
        sleep(0.1)

        if curr_button != button_sensor() and button_sensor() == 1:
            button_toggle_on()

        curr_door = update('door', curr_door, door_sensor())
        curr_button = update('button', curr_button, button_sensor())
        curr_motion = update('motion', curr_motion, motion_sensor())
