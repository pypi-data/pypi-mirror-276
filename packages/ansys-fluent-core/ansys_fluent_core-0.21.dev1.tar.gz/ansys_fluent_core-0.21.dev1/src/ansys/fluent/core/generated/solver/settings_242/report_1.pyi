#
# This is an auto-generated file.  DO NOT EDIT!
#


from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    _CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    _HasAllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from typing import Union, List, Tuple

from .electrolyte_area import electrolyte_area as electrolyte_area_cls
from .monitor_enable import monitor_enable as monitor_enable_cls
from .monitor_frequency import monitor_frequency as monitor_frequency_cls

class report(Group):
    fluent_name = ...
    child_names = ...
    electrolyte_area: electrolyte_area_cls = ...
    monitor_enable: monitor_enable_cls = ...
    monitor_frequency: monitor_frequency_cls = ...
