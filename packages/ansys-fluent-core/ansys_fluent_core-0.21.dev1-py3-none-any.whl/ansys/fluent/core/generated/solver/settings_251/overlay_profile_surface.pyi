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

from .overlay_1 import overlay as overlay_cls
from .profile_name_1 import profile_name as profile_name_cls
from .graphics_object import graphics_object as graphics_object_cls
from .field_contour import field_contour as field_contour_cls
from .filed_variable import filed_variable as filed_variable_cls

class overlay_profile_surface(Command):
    fluent_name = ...
    argument_names = ...
    overlay: overlay_cls = ...
    profile_name: profile_name_cls = ...
    graphics_object: graphics_object_cls = ...
    field_contour: field_contour_cls = ...
    filed_variable: filed_variable_cls = ...
