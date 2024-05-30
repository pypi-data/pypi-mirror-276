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

from .trim_option import trim_option as trim_option_cls
from .update_frequency import update_frequency as update_frequency_cls
from .damping_factor import damping_factor as damping_factor_cls
from .thrust_coefficient import thrust_coefficient as thrust_coefficient_cls
from .x_moment_coefficient import x_moment_coefficient as x_moment_coefficient_cls
from .y_moment_coefficient import y_moment_coefficient as y_moment_coefficient_cls

class trimming(Group):
    fluent_name = ...
    child_names = ...
    trim_option: trim_option_cls = ...
    update_frequency: update_frequency_cls = ...
    damping_factor: damping_factor_cls = ...
    thrust_coefficient: thrust_coefficient_cls = ...
    x_moment_coefficient: x_moment_coefficient_cls = ...
    y_moment_coefficient: y_moment_coefficient_cls = ...
