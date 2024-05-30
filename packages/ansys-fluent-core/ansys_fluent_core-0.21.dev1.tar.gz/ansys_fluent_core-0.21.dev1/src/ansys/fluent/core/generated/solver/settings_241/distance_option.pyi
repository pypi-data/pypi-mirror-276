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

from .option import option as option_cls
from .cell_distance import cell_distance as cell_distance_cls
from .normal_distance import normal_distance as normal_distance_cls
from .volume_distance import volume_distance as volume_distance_cls

class distance_option(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    cell_distance: cell_distance_cls = ...
    normal_distance: normal_distance_cls = ...
    volume_distance: volume_distance_cls = ...
