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

from .distance_option import distance_option as distance_option_cls
from .boundary_list import boundary_list as boundary_list_cls
from .create_volume_surface import create_volume_surface as create_volume_surface_cls

class boundary(Group):
    fluent_name = ...
    child_names = ...
    distance_option: distance_option_cls = ...
    boundary_list: boundary_list_cls = ...
    create_volume_surface: create_volume_surface_cls = ...
