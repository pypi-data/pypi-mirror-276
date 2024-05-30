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

from .pressure_jump_specification import pressure_jump_specification as pressure_jump_specification_cls
from .swirl_velocity_specification import swirl_velocity_specification as swirl_velocity_specification_cls
from .geometry_3 import geometry as geometry_cls

class phase_child(Group):
    fluent_name = ...
    child_names = ...
    pressure_jump_specification: pressure_jump_specification_cls = ...
    swirl_velocity_specification: swirl_velocity_specification_cls = ...
    geometry: geometry_cls = ...
