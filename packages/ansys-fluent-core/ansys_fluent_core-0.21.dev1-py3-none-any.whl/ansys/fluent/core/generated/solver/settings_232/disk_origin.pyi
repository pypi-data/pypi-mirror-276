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

from .disk_origin_x import disk_origin_x as disk_origin_x_cls
from .disk_origin_y import disk_origin_y as disk_origin_y_cls
from .disk_origin_z import disk_origin_z as disk_origin_z_cls

class disk_origin(Group):
    fluent_name = ...
    child_names = ...
    disk_origin_x: disk_origin_x_cls = ...
    disk_origin_y: disk_origin_y_cls = ...
    disk_origin_z: disk_origin_z_cls = ...
