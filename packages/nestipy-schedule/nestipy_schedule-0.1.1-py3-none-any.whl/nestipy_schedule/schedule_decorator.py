from typing import Callable, Union, Any, Type

from nestipy.metadata import SetMetadata

from .schedule_metadata import ScheduleMetadata, ScheduleData


def Cron(cron: str, timezone: str = None, name: str = None) -> Callable[[Union[Type, Callable[..., Any]]], Any]:
    return SetMetadata(ScheduleMetadata.Schedule, ScheduleData(ScheduleMetadata.Cron, cron, timezone, name))


def Interval(seconds: int, timezone: str = None, name: str = None):
    return SetMetadata(ScheduleMetadata.Schedule, ScheduleData(ScheduleMetadata.Interval, seconds, timezone, name))


def Timeout(milliseconds: int, timezone: str = None, name: str = None):
    return SetMetadata(ScheduleMetadata.Schedule, ScheduleData(ScheduleMetadata.Timeout, milliseconds, timezone, name))
