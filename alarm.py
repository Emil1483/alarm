try:

    import RPi.GPIO as GPIO
    from time import sleep
    from datetime import datetime, timedelta

    GPIO.setmode(GPIO.BOARD)

    from speaker import *
    from sensor import *
    from action import *

    notification()

    with open('school_start.txt', 'r') as f:
        start_time_string = f.read().strip()
        start_time = datetime.strptime(start_time_string, '%d/%m/%Y %H:%M')

        duration = start_time - datetime.now()

        if duration > timedelta(hours=12):
            print(f'Next alarm at {time} is too long to wait. Aborting')
            GPIO.cleanup()
            quit()

        print(f'School starts in {duration}')

        max_duration = max(action.duration for action in actions)

        sleep_time = start_time - datetime.now() - max_duration

        sleep(sleep_time.total_seconds())

        curr = sensor()
        while curr == sensor():
            duration = start_time - datetime.now()
            for action in actions:
                if action.duration > duration:

                    action.run()
                    actions.remove(action)

            sleep(1)

    clean_up()

except Exception as e:
    clean_up()
    print(e)
