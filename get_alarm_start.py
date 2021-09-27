from datetime import datetime, timedelta
from get_visma_cookie import get_visma_cookie
import requests

url = 'https://valler-vgs.inschool.visma.no/control/timetablev2/learner/7191143/fetch/ALL/0/current'

tomorrow = datetime.now() + timedelta(days=1)
tomorrow_string = tomorrow.strftime('%d/%m/%Y')

params = {
    'forWeek': tomorrow_string,
    'extra-info': True,
    'types':
    'LESSON,EVENT,ACTIVITY,SUBSTITUTION',
    '_': tomorrow.timestamp()
}

headers = {'cookie': get_visma_cookie()}

response = requests.get(url, params=params, headers=headers)
json = response.json()

timetableItems = json['timetableItems']

lessons = [e for e in timetableItems if e['date'] == tomorrow_string]

if len(lessons) == 0:
    with open('alarm_start.txt', 'w') as f:
        f.write('')
    quit()

start = min(e['startTime'] for e in lessons)

with open('alarm_start.txt', 'w') as f:
    f.write(f'{tomorrow_string} {start}')
