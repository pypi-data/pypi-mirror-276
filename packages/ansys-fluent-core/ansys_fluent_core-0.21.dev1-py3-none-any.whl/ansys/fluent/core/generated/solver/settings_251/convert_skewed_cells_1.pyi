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

from .cell_thread_list import cell_thread_list as cell_thread_list_cls
from .max_cell_skewness import max_cell_skewness as max_cell_skewness_cls
from .convert_skewed_cells import convert_skewed_cells as convert_skewed_cells_cls

class convert_skewed_cells(Command):
    fluent_name = ...
    argument_names = ...
    cell_thread_list: cell_thread_list_cls = ...
    max_cell_skewness: max_cell_skewness_cls = ...
    convert_skewed_cells: convert_skewed_cells_cls = ...
