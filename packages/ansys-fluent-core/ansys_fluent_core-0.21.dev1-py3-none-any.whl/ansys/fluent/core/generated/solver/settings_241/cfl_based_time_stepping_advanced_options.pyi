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

from .control_time_step_size_variation import control_time_step_size_variation as control_time_step_size_variation_cls
from .use_average_cfl import use_average_cfl as use_average_cfl_cls
from .cfl_type import cfl_type as cfl_type_cls

class cfl_based_time_stepping_advanced_options(Group):
    fluent_name = ...
    child_names = ...
    control_time_step_size_variation: control_time_step_size_variation_cls = ...
    use_average_cfl: use_average_cfl_cls = ...
    cfl_type: cfl_type_cls = ...
