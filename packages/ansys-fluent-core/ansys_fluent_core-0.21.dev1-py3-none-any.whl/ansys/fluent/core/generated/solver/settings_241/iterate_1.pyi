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

from .iter_count_4 import iter_count as iter_count_cls
from .time_steps_count import time_steps_count as time_steps_count_cls
from .iter_per_time_step_count import iter_per_time_step_count as iter_per_time_step_count_cls

class iterate(Command):
    fluent_name = ...
    argument_names = ...
    iter_count: iter_count_cls = ...
    time_steps_count: time_steps_count_cls = ...
    iter_per_time_step_count: iter_per_time_step_count_cls = ...
