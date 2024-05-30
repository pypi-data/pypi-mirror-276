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

from .multi_level_grid import multi_level_grid as multi_level_grid_cls
from .residual_reduction_level import residual_reduction_level as residual_reduction_level_cls
from .cycle_count import cycle_count as cycle_count_cls

class customize_fmg_initialization(Command):
    fluent_name = ...
    argument_names = ...
    multi_level_grid: multi_level_grid_cls = ...
    residual_reduction_level: residual_reduction_level_cls = ...
    cycle_count: cycle_count_cls = ...
