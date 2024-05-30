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

from .option_13 import option as option_cls
from .min_allowed import min_allowed as min_allowed_cls
from .max_allowed import max_allowed as max_allowed_cls
from .wall_zones import wall_zones as wall_zones_cls
from .phase_27 import phase as phase_cls

class yplus_star(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    min_allowed: min_allowed_cls = ...
    max_allowed: max_allowed_cls = ...
    wall_zones: wall_zones_cls = ...
    phase: phase_cls = ...
