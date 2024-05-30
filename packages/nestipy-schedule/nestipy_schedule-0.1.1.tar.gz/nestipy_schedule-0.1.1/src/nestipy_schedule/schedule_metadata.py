import dataclasses
from typing import Union


class ScheduleMetadata:
    Schedule: str = '__schedule__'
    Cron: str = '__schedule__cron__'
    Interval: str = '__schedule__interval__'
    Timeout: str = '__schedule__timeout__'


@dataclasses.dataclass
class ScheduleData:
    schedule: str
    value: Union[str, int]
    timezone: Union[str, None] = None
    name: Union[str, None] = None
