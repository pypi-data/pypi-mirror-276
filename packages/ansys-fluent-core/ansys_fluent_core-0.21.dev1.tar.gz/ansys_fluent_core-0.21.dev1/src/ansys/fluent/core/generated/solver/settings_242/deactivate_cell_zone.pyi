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

from .cell_deactivate_list import cell_deactivate_list as cell_deactivate_list_cls

class deactivate_cell_zone(Command):
    fluent_name = ...
    argument_names = ...
    cell_deactivate_list: cell_deactivate_list_cls = ...
