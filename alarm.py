import subprocess
import sys
from datetime import datetime, timedelta
from time import sleep

from action import action as a
from sensor import sensor
from settings import settings
from speaker import speaker
from weather.weather import weather


def main(test=False):

    speaker.notification()

    start_time = settings().school_start
    max_duration = max(action.duration for action in a.actions)

    if test:
        start_time = datetime.now() + max_duration

    if start_time is None:
        print('School start is set to None. Aborting')
        a.clean_up()
        quit()

    duration = start_time - datetime.now()

    if duration > timedelta(hours=12):
        print(f'Next alarm at {start_time} is too long to wait. Aborting')
        a.clean_up()
        quit()

    if duration < timedelta():
        print('Looks like school started in the past. Aborting')
        a.clean_up()
        quit()

    print(f'School starts in {duration}')

    sleep_time = start_time - datetime.now() - max_duration
    sleep_time_seconds = sleep_time.total_seconds()

    if sleep_time_seconds > 0:
        sleep(sleep_time_seconds)

    curr = sensor.door_sensor()
    while curr == sensor.door_sensor():
        duration = start_time - datetime.now()
        for action in a.actions:
            if action.duration > duration:

                print(f'running {action.name}')
                action.run()
                a.actions.remove(action)

        sleep(1)

    a.clean_up()

    subprocess.run(['espeak', weather()])

    subprocess.run(['sudo', 'reboot'])


if __name__ == '__main__':
    try:
        main(test='--test' in sys.argv)
    except Exception as e:
        a.clean_up()
        print(type(e), e)
        raise e
