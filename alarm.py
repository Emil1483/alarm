try:

    from time import sleep
    from datetime import datetime, timedelta
    import subprocess
    import sys

    from speaker import speaker
    from sensor import sensor
    from action import action as a
    from settings import settings
    
    from weather.weather import weather

    speaker.notification()

    start_time = settings().school_start
    max_duration = max(action.duration for action in a.actions)

    if start_time is None:
        print('School start is set to None. Aborting')
        a.clean_up()
        quit()

    if '--test' in sys.argv:
        start_time = datetime.now() + max_duration

    duration = start_time - datetime.now()

    if duration > timedelta(hours=12):
        print(f'Next alarm at {time} is too long to wait. Aborting')
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

except Exception as e:
    a.clean_up()
    print(type(e), e)
    raise e
