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

from .max_fine_relaxations import max_fine_relaxations as max_fine_relaxations_cls
from .max_coarse_relaxations import max_coarse_relaxations as max_coarse_relaxations_cls

class flexible_cycle_paramters(Group):
    fluent_name = ...
    child_names = ...
    max_fine_relaxations: max_fine_relaxations_cls = ...
    max_coarse_relaxations: max_coarse_relaxations_cls = ...
