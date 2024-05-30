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

from .speed_1 import speed as speed_cls
from .rotation_axis import rotation_axis as rotation_axis_cls

class rotational_velocity(Group):
    fluent_name = ...
    child_names = ...
    speed: speed_cls = ...
    rotation_axis: rotation_axis_cls = ...
