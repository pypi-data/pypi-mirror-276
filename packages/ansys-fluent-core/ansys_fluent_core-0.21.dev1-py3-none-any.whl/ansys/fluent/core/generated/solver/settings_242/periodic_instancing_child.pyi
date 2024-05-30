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

from .name_12 import name as name_cls
from .periodic_type import periodic_type as periodic_type_cls
from .surfaces_12 import surfaces as surfaces_cls
from .translation_1 import translation as translation_cls
from .rotation import rotation as rotation_cls
from .axis_origin_4 import axis_origin as axis_origin_cls
from .rotation_angle_1 import rotation_angle as rotation_angle_cls
from .repeats import repeats as repeats_cls
from .display_6 import display as display_cls

class periodic_instancing_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    periodic_type: periodic_type_cls = ...
    surfaces: surfaces_cls = ...
    translation: translation_cls = ...
    rotation: rotation_cls = ...
    axis_origin: axis_origin_cls = ...
    rotation_angle: rotation_angle_cls = ...
    repeats: repeats_cls = ...
    command_names = ...

    def display(self, ):
        """
        Display periodic instancing.
        """

