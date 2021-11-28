if __name__ == '__main__':
    from get_yr_data import get_data
else:
    from weather.get_yr_data import get_data


def weather():
    data = get_data()
    properties = data['properties']
    meta = properties['meta']
    units = meta['units']
    timeseries = properties['timeseries']

    weather = timeseries[0]['data']

    weather_now = weather['instant']['details']
    weather_next_1_hours = weather['next_1_hours']['details']
    weather_next_6_hours = weather['next_6_hours']['details']

    def readable_details(details, formatter):
        result = ''
        for key, value in details.items():
            result += formatter(key.replace('_', ' '), f'{value} {units[key]}')
            result += '\n'

        return result
    
    result = ''

    result += readable_details(weather_now, lambda key, value:
                           f'The current {key} is {value}.')

    result += readable_details(weather_next_1_hours, lambda key, value:
                           f'For the next hour, {key} is {value}.')

    result += readable_details(weather_next_6_hours, lambda key, value:
                           f'For the next 6 hours, {key} is {value}.')
    
    return result[:-1]


if __name__ == '__main__':
    print(weather())

