import json
import os
from datetime import datetime, date
from dataclasses import dataclass, asdict

def deserialize(key, json, cls, allowed_types, fallback):
    if not key in json or json[key] is None: return None
    
    if isinstance(json[key], cls): return json[key]
    
    if type(json[key]) not in allowed_types:
        raise ValueError(f'{key} of type {type(json[key])} must be one of types {allowed_types}')

    try:
        return fallback(json[key])
    except Exception as e:
        raise ValueError(f'Was not able to deserialize {key} ({json[key]}). Error: ({e})')

@dataclass(frozen=True, order=True)
class Settings:
    school_start: datetime.date = None

    def to_dict(self):
        result = asdict(self)
        
        if self.school_start is not None:
            result['school_start'] = self.school_start.strftime('%d/%m/%Y %H:%M')

        return result
    
    @classmethod
    def from_dict(_, json):
        return Settings(
            school_start=deserialize('school_start', json, date, [date, str],
                lambda value: datetime.strptime(value, '%d/%m/%Y %H:%M')
            )
        )

    @classmethod
    def fromSettings(_, settings):
        return Settings.from_dict(settings.to_dict())

    def check_school_start(self):
        if self.school_start is None: return
        
        if not isinstance(self.school_start, date):
            raise TypeError(f'school_start {self.school_start} must be a datetime')
        
        if self.school_start < datetime.now():
            raise ValueError(f'school_start {self.school_start} must be in the future')

    def validate(self):
        self.check_school_start()

def path():
    return os.path.dirname(os.path.realpath(__file__))

def settings():
    if os.path.exists(f'{path()}/settings.json'):
        with open(f'{path()}/settings.json', 'r') as s:
            settings_dict = json.load(s)
            return Settings.from_dict(settings_dict)

    with open(f'{path()}/settings.json', 'w') as s:
        json.dump(Settings().to_dict(), s, indent=4)
        return Settings()

def update(**kwargs):
    settings_dict = settings().to_dict()
    not_allowed_keys = [key for key in kwargs.keys() if key not in settings_dict.keys()]
    if len(not_allowed_keys) > 0:
        raise ValueError(f'{not_allowed_keys} are not allowed keys')
    
    for key, value in kwargs.items():
        settings_dict[key] = value

    result = Settings.from_dict(settings_dict)
    result.validate()

    with open(f'{path()}/settings.json', 'w') as s:
        json.dump(result.to_dict(), s, indent=4)

    print('current settings:')
    print(settings())

if __name__ == '__main__':
    print(settings())
