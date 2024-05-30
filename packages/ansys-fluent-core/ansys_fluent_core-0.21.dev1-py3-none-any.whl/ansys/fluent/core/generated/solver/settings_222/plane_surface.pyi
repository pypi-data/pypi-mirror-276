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

from .plane_surface_child import plane_surface_child


class plane_surface(NamedObject[plane_surface_child], _CreatableNamedObjectMixin[plane_surface_child]):
    fluent_name = ...
    child_object_type = ...
