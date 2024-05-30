from dataclasses import dataclass

from nestipy.dynamic_module import ConfigurableModuleBuilder


@dataclass
class ScheduleOption:
    pass


ConfigurableModuleClass, SCHEDULE_OPTION = ConfigurableModuleBuilder[ScheduleOption]().set_method(
    'for_root').build()
