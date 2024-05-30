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

from .enabled_4 import enabled as enabled_cls
from .tolerance import tolerance as tolerance_cls
from .max_num_refinements import max_num_refinements as max_num_refinements_cls
from .step_size_fraction import step_size_fraction as step_size_fraction_cls

class accuracy_control(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    tolerance: tolerance_cls = ...
    max_num_refinements: max_num_refinements_cls = ...
    step_size_fraction: step_size_fraction_cls = ...
