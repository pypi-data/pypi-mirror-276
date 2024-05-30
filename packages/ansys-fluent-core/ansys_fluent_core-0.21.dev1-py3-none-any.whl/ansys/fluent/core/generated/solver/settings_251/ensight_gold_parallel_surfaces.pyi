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

from .file_name_1 import file_name as file_name_cls
from .binary_format import binary_format as binary_format_cls
from .surfaces import surfaces as surfaces_cls
from .cell_centered import cell_centered as cell_centered_cls
from .cell_function import cell_function as cell_function_cls

class ensight_gold_parallel_surfaces(Command):
    fluent_name = ...
    argument_names = ...
    file_name: file_name_cls = ...
    binary_format: binary_format_cls = ...
    surfaces: surfaces_cls = ...
    cell_centered: cell_centered_cls = ...
    cell_function: cell_function_cls = ...
