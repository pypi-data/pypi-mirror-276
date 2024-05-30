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
from .thrust_coef import thrust_coef as thrust_coef_cls
from .pitch_moment_coef import pitch_moment_coef as pitch_moment_coef_cls
from .roll_moment_coef import roll_moment_coef as roll_moment_coef_cls

class trimming(Group):
    fluent_name = ...
    child_names = ...
    trim_option: trim_option_cls = ...
    update_frequency: update_frequency_cls = ...
    damping_factor: damping_factor_cls = ...
    thrust_coef: thrust_coef_cls = ...
    pitch_moment_coef: pitch_moment_coef_cls = ...
    roll_moment_coef: roll_moment_coef_cls = ...
