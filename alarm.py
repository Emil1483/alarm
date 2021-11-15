try:

    from time import sleep
    from datetime import datetime, timedelta

    from speaker import speaker
    from sensor import sensor
    from action import action as a

    speaker.notification()

    with open('school_start/school_start.txt', 'r') as f:
        start_time_string = f.read().strip()
        start_time = datetime.strptime(start_time_string, '%d/%m/%Y %H:%M')

        #start_time = datetime.now() + timedelta(minutes=90)

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

        max_duration = max(action.duration for action in a.actions)

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

except Exception as e:
    a.clean_up()
    print(e)
