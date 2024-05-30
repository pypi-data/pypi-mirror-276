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

from .target_type import target_type as target_type_cls
from .number_of_cells import number_of_cells as number_of_cells_cls
from .factor_of_cells import factor_of_cells as factor_of_cells_cls

class target(Group):
    fluent_name = ...
    child_names = ...
    target_type: target_type_cls = ...
    number_of_cells: number_of_cells_cls = ...
    factor_of_cells: factor_of_cells_cls = ...
