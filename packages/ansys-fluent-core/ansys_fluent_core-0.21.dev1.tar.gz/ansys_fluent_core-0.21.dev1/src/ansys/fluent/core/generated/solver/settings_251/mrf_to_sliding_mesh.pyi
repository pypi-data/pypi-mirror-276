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

from .cell_zone_name import cell_zone_name as cell_zone_name_cls

class mrf_to_sliding_mesh(Command):
    fluent_name = ...
    argument_names = ...
    cell_zone_name: cell_zone_name_cls = ...
