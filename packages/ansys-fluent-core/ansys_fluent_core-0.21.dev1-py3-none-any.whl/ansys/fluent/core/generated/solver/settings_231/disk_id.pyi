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

from .embedded_face_zone import embedded_face_zone as embedded_face_zone_cls
from .floating_surface import floating_surface as floating_surface_cls

class disk_id(Group):
    fluent_name = ...
    child_names = ...
    embedded_face_zone: embedded_face_zone_cls = ...
    floating_surface: floating_surface_cls = ...
