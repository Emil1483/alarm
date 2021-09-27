try:

    import RPi.GPIO as GPIO
    from time import sleep
    from datetime import datetime, timedelta

    GPIO.setmode(GPIO.BOARD)

    from speaker import *
    from sensor import *

    with open('alarm_start.txt', 'r') as f:
        time_string = f.read().strip()
        time = datetime.strptime(time_string, '%d/%m/%Y %H:%M')
        duration = time - datetime.now() - timedelta(minutes=30)

        if duration > timedelta(hours=12):
            print(f'next alarm at {time} is too long to wait. Aborting')
            GPIO.cleanup()
            quit()

        print(f'Alarm will fire in {duration}')

        sleep(duration.total_seconds())

    curr = sensor()
    alarm_until(lambda : sensor() != curr)

    GPIO.cleanup()

except Exception as e:
    GPIO.cleanup()
    print(e)
