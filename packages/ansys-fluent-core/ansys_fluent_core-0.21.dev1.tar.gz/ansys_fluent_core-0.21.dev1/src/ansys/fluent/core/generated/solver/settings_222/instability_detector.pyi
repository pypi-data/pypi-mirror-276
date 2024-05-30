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

from .enable_instability_detector import enable_instability_detector as enable_instability_detector_cls
from .set_cfl_limit import set_cfl_limit as set_cfl_limit_cls
from .set_cfl_type import set_cfl_type as set_cfl_type_cls
from .set_velocity_limit import set_velocity_limit as set_velocity_limit_cls
from .unstable_event_outer_iterations import unstable_event_outer_iterations as unstable_event_outer_iterations_cls

class instability_detector(Group):
    fluent_name = ...
    child_names = ...
    enable_instability_detector: enable_instability_detector_cls = ...
    set_cfl_limit: set_cfl_limit_cls = ...
    set_cfl_type: set_cfl_type_cls = ...
    set_velocity_limit: set_velocity_limit_cls = ...
    unstable_event_outer_iterations: unstable_event_outer_iterations_cls = ...
