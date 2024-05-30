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

from .enabled_9 import enabled as enabled_cls
from .enhanced_formulation_enabled import enhanced_formulation_enabled as enhanced_formulation_enabled_cls
from .constant_during_iterations import constant_during_iterations as constant_during_iterations_cls
from .limiter import limiter as limiter_cls

class linearization(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    enhanced_formulation_enabled: enhanced_formulation_enabled_cls = ...
    constant_during_iterations: constant_during_iterations_cls = ...
    limiter: limiter_cls = ...
