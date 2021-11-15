try:

    from datetime import datetime, timedelta
    from get_visma_lessons import get_visma_lessons, tomorrow_string
    import requests
    
    json = get_visma_lessons()

    timetableItems = json['timetableItems']

    lessons = [e for e in timetableItems if e['date'] == tomorrow_string]

    if len(lessons) == 0:
        with open('alarm_start.txt', 'w') as f:
            f.write('')
        quit()

    start = min(e['startTime'] for e in lessons)

    with open('school_start.txt', 'w') as f:
        result = f'{tomorrow_string} {start}'

        print(f'school starts at {result}')

        f.write(result)

except Exception as e:
    print(e)
