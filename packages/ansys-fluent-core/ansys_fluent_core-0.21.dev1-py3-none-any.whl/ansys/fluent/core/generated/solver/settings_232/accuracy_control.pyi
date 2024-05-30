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

from .option_4 import option as option_cls
from .tolerance import tolerance as tolerance_cls
from .max_number_of_refinements import max_number_of_refinements as max_number_of_refinements_cls
from .number_of_cells_to_cross import number_of_cells_to_cross as number_of_cells_to_cross_cls

class accuracy_control(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    tolerance: tolerance_cls = ...
    max_number_of_refinements: max_number_of_refinements_cls = ...
    number_of_cells_to_cross: number_of_cells_to_cross_cls = ...
