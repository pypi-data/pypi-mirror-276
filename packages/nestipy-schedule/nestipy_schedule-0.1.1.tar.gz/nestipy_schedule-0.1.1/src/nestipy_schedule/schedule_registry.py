from datetime import datetime
from typing import Any

from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.base import BaseTrigger

from nestipy.common import Injectable


class _Undefined(object):
    def __nonzero__(self):
        return False

    def __bool__(self):
        return False

    def __repr__(self):
        return '<undefined>'


undefined = _Undefined()


@Injectable()
class SchedulerRegistry(AsyncIOScheduler):
    def __init__(self):
        super().__init__(gconfig={}, **{})
