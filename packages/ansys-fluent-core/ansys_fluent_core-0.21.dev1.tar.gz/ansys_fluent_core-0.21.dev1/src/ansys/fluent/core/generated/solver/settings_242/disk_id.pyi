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
from .floating_surface_name import floating_surface_name as floating_surface_name_cls
from .create_floating_disk import create_floating_disk as create_floating_disk_cls

class disk_id(Group):
    fluent_name = ...
    child_names = ...
    embedded_face_zone: embedded_face_zone_cls = ...
    floating_surface_name: floating_surface_name_cls = ...
    command_names = ...

    def create_floating_disk(self, ):
        """
        'create_floating_disk' command.
        """

