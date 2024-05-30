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

from .method import method as method_cls
from .samp_time_period import samp_time_period as samp_time_period_cls
from .samp_time_steps import samp_time_steps as samp_time_steps_cls
from .avg_time_period import avg_time_period as avg_time_period_cls
from .avg_time_steps import avg_time_steps as avg_time_steps_cls

class statistics_controls(Command):
    fluent_name = ...
    argument_names = ...
    method: method_cls = ...
    samp_time_period: samp_time_period_cls = ...
    samp_time_steps: samp_time_steps_cls = ...
    avg_time_period: avg_time_period_cls = ...
    avg_time_steps: avg_time_steps_cls = ...
