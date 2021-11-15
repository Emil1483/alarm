from hue_api import HueApi
from time import sleep
from datetime import datetime, timedelta, time
import requests

from sensor import sensor as s

def wait_for_internet():
    while True:
        try:
            requests.get('https://www.google.com', timeout=1)
            return
        except Exception:
            pass

wait_for_internet()

api = HueApi()
#api.create_new_user('192.168.10.178')
#api.save_api_key()
api.load_existing()

api.fetch_lights()

def hue_is_on():
    api.fetch_lights()
    return any(light.state.is_on for light in api.lights)

def hue_on(h = 43425, sa = 254, b = 200):
    print('hue on')

    s.button_set_on(True)
    
    for light in api.lights:
        # state = light.state
        # print(state.brightness, state.saturation, state.hue)

        light.set_on()
        light.set_color(h, sa)
        light.set_brightness(b)
        
        sleep(0.5)

def hue_off():
    print('hue off')
    s.button_set_on(False)
    api.turn_off(range(len(api.lights) + 1))

if __name__ == '__main__':
    import sys

    hue_off()

    curr_door = s.door_sensor()
    curr_button = s.button_sensor()
    last_change = datetime.now() - timedelta(hours=1)
    last_opened = datetime.now() - timedelta(hours=1)
    last_button_press = datetime.now() - timedelta(hours=1)

    def print_state():
        print('opening door:', curr_door == 0,
              'hue is on:', hue_is_on(),
              'button is on', s.button_is_on,
              'time since last change', datetime.now() - last_change,
              'time since last opened', datetime.now() - last_opened,
              'time since last button press', datetime.now() - last_button_press)

    def on_button_update():
        global curr_door, curr_button, last_change, last_opened, last_button_press

        curr_button = s.button_sensor()

        if curr_button == False: return

        print_state()

        last_change = datetime.now()
        last_button_press = datetime.now()
        
        if hue_is_on():
            hue_off()
        else:
            hue_on()

    def on_door_update():
        global curr_door, curr_button, last_change, last_opened, last_button_press

        tomorrow = datetime.now() + timedelta(days=1)
        time_until_end_of_day = datetime.combine(tomorrow, time.min) - datetime.now()
        time_since_start_of_day = timedelta(days=1) - time_until_end_of_day

        if time_until_end_of_day < timedelta(hours=2, minutes=30): return
        if time_since_start_of_day < timedelta(hours=6): return

        curr_door = s.door_sensor()
        time_since_last_change = datetime.now() - last_change
        time_since_last_opened = datetime.now() - last_opened
        time_since_last_button_press = datetime.now() - last_button_press

        print_state()

        opening_door = curr_door == 0

        if opening_door:
            last_opened = datetime.now()

        if time_since_last_button_press < timedelta(seconds=60):
            return

        if (opening_door or time_since_last_opened > timedelta(seconds=60)) and not hue_is_on():
            last_change = datetime.now()
            hue_on()

        if (not opening_door and hue_is_on() and
                time_since_last_change > timedelta(seconds=60) and
                time_since_last_opened < timedelta(seconds=10)):
            last_change = datetime.now()
            hue_off()

    i = 0
    delay = 0.05
    while True:
        sleep(delay)

        if i % (1 // delay) == 0:
            s.button_set_on(hue_is_on())

        if curr_door != s.door_sensor():
            on_door_update()

        if curr_button != s.button_sensor():
            on_button_update()

        i += 1
