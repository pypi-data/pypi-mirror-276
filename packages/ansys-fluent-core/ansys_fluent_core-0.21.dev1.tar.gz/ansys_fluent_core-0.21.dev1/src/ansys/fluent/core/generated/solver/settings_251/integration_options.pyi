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

from .absolute_ode_tolerance import absolute_ode_tolerance as absolute_ode_tolerance_cls
from .relative_ode_tolerance import relative_ode_tolerance as relative_ode_tolerance_cls

class integration_options(Group):
    fluent_name = ...
    child_names = ...
    absolute_ode_tolerance: absolute_ode_tolerance_cls = ...
    relative_ode_tolerance: relative_ode_tolerance_cls = ...
