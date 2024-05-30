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

from .name import name as name_cls
from .reference_frame import reference_frame as reference_frame_cls
from .point import point as point_cls
from .snap_method import snap_method as snap_method_cls
from .display_3 import display as display_cls

class point_surface_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    reference_frame: reference_frame_cls = ...
    point: point_cls = ...
    snap_method: snap_method_cls = ...
    command_names = ...

    def display(self, ):
        """
        'display' command.
        """

