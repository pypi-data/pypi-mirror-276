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

from .basic_info import basic_info as basic_info_cls
from .disk_origin import disk_origin as disk_origin_cls
from .disk_orientation import disk_orientation as disk_orientation_cls
from .disk_id import disk_id as disk_id_cls
from .blade_pitch_angles import blade_pitch_angles as blade_pitch_angles_cls
from .blade_flap_angles import blade_flap_angles as blade_flap_angles_cls
from .tip_loss import tip_loss as tip_loss_cls

class general(Group):
    fluent_name = ...
    child_names = ...
    basic_info: basic_info_cls = ...
    disk_origin: disk_origin_cls = ...
    disk_orientation: disk_orientation_cls = ...
    disk_id: disk_id_cls = ...
    blade_pitch_angles: blade_pitch_angles_cls = ...
    blade_flap_angles: blade_flap_angles_cls = ...
    tip_loss: tip_loss_cls = ...
