import json
from datetime import datetime
import os

import pytz
import requests
from dateutil.parser import parse

url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact'


def get_data():
    data = None
    if os.path.exists('cache.json'):
        with open('cache.json', 'r') as f:
            data = json.load(f)

        expires = parse(data['headers']['Expires'])
        now = datetime.now(tz=pytz.timezone('Europe/Oslo'))
        expired = now > expires

        if not expired:
            return data['json']

    last_modified = None if data is None else data['headers']['Last-Modified']

    params = {'lat': 59.8561, 'lon': 10.4567}
    headers = {
        'User-Agent': 'DjupvikAlarm/1.0',
    }
    if last_modified is not None:
        headers['If-Modified-Since'] = last_modified

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 304:
        return data['json']

    with open('cache.json', 'w') as f:
        cache = {
            'headers': dict(response.headers),
            'json': response.json(),
        }
        json.dump(cache, f, indent=4)

    return response.json()


if __name__ == '__main__':
    print(get_data())

