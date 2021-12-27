try:
    import sys
    sys.path.append('..')

    from datetime import datetime, timedelta
    from get_visma_lessons import get_visma_lessons, tomorrow_string
    from settings import update
    import requests
    
    json = get_visma_lessons()

    timetableItems = json['timetableItems']

    lessons = [e for e in timetableItems if e['date'] == tomorrow_string]

    if len(lessons) == 0:
        with open('alarm_start.txt', 'w') as f:
            f.write('')

        print('looks like there are no lessons')

        update(school_start=None)

        quit()

    start = min(e['startTime'] for e in lessons)

    result_string = f'{tomorrow_string} {start}'
    result = datetime.strptime(result_string, '%d/%m/%Y %H:%M')

    print(f'school starts at {result_string}')

    update(school_start=result)

except Exception as e:
    print(type(e), e)
