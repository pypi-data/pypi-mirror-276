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

from .cell_zone_name_1 import cell_zone_name as cell_zone_name_cls
from .move_cells import move_cells as move_cells_cls

class sep_cell_zone_region(Command):
    fluent_name = ...
    argument_names = ...
    cell_zone_name: cell_zone_name_cls = ...
    move_cells: move_cells_cls = ...
