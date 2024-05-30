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

from .terminology import terminology as terminology_cls
from .disk_normal_x import disk_normal_x as disk_normal_x_cls
from .disk_normal_y import disk_normal_y as disk_normal_y_cls
from .disk_normal_z import disk_normal_z as disk_normal_z_cls
from .disk_pitch_angle import disk_pitch_angle as disk_pitch_angle_cls
from .disk_bank_angle import disk_bank_angle as disk_bank_angle_cls

class disk_orientation(Group):
    fluent_name = ...
    child_names = ...
    terminology: terminology_cls = ...
    disk_normal_x: disk_normal_x_cls = ...
    disk_normal_y: disk_normal_y_cls = ...
    disk_normal_z: disk_normal_z_cls = ...
    disk_pitch_angle: disk_pitch_angle_cls = ...
    disk_bank_angle: disk_bank_angle_cls = ...
