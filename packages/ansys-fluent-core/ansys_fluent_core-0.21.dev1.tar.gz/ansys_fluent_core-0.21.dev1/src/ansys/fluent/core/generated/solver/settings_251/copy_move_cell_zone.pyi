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
from .translate import translate as translate_cls
from .rotation_angle import rotation_angle as rotation_angle_cls
from .offset import offset as offset_cls
from .axis import axis as axis_cls

class copy_move_cell_zone(Command):
    fluent_name = ...
    argument_names = ...
    cell_zone_name: cell_zone_name_cls = ...
    translate: translate_cls = ...
    rotation_angle: rotation_angle_cls = ...
    offset: offset_cls = ...
    axis: axis_cls = ...
