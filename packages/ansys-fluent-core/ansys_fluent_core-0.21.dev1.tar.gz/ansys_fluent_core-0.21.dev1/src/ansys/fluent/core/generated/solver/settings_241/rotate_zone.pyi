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

from .zone_names_2 import zone_names as zone_names_cls
from .rotation_angle import rotation_angle as rotation_angle_cls
from .origin import origin as origin_cls
from .axis import axis as axis_cls

class rotate_zone(Command):
    fluent_name = ...
    argument_names = ...
    zone_names: zone_names_cls = ...
    rotation_angle: rotation_angle_cls = ...
    origin: origin_cls = ...
    axis: axis_cls = ...
