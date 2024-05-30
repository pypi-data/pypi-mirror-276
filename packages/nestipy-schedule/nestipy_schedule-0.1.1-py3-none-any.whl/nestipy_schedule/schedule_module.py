import inspect
from datetime import datetime, timedelta
from typing import Annotated

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from nestipy.common import Module
from nestipy.core import DiscoverService
from nestipy.dynamic_module import NestipyModule
from nestipy.ioc import Inject
from nestipy.metadata import Reflect

from .schedule_builder import ConfigurableModuleClass, ScheduleOption, SCHEDULE_OPTION
from .schedule_metadata import ScheduleMetadata, ScheduleData
from .schedule_registry import SchedulerRegistry


@Module(
    providers=[SchedulerRegistry],
    exports=[SchedulerRegistry]
)
class ScheduleModule(ConfigurableModuleClass, NestipyModule):
    _config: Annotated[ScheduleOption, Inject(SCHEDULE_OPTION)]
    _discovery: Annotated[DiscoverService, Inject()]
    _registry: Annotated[SchedulerRegistry, Inject()]

    async def on_startup(self):
        self.setup_all_jobs()
        self._registry.start()

    async def on_shutdown(self):
        self._registry.shutdown(wait=False)

    @classmethod
    def _is_schedule(cls, method: callable):
        return Reflect.get_metadata(method, ScheduleMetadata.Schedule, None) is not None

    def add_job(self, method: callable):
        schedule: ScheduleData = Reflect.get_metadata(
            method, ScheduleMetadata.Schedule,
            ScheduleData(ScheduleMetadata.Timeout, 5000)
        )
        match schedule.schedule:
            case ScheduleMetadata.Cron:
                trigger = CronTrigger.from_crontab(schedule.value, timezone=schedule.timezone)
                return self._registry.add_job(method, trigger=trigger, id=schedule.name)
            case ScheduleMetadata.Interval:
                trigger = IntervalTrigger(seconds=schedule.value, timezone=schedule.timezone)
                return self._registry.add_job(method, trigger=trigger, id=schedule.name)
            case ScheduleMetadata.Timeout:
                run_date = datetime.now(tz=schedule.timezone) + timedelta(milliseconds=schedule.value)
                trigger = DateTrigger(run_date=run_date, timezone=schedule.timezone)
                return self._registry.add_job(method, trigger=trigger, id=schedule.name)

    def setup_all_jobs(self):
        instances = self._discovery.get_all_controller() + self._discovery.get_all_provider()
        for p in instances:
            elements = inspect.getmembers(p, lambda a: inspect.isfunction(a) or inspect.iscoroutinefunction(a))
            methods = [
                method for (method, _) in elements
                if not method.startswith("__") and self._is_schedule(getattr(p, method))
            ]
            for m in methods:
                self.add_job(getattr(p, m))
