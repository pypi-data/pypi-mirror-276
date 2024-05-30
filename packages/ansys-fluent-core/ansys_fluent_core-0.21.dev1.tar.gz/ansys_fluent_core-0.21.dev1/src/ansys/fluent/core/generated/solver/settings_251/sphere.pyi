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

from .center import center as center_cls
from .radius import radius as radius_cls
from .inside import inside as inside_cls
from .create_volume_surface import create_volume_surface as create_volume_surface_cls

class sphere(Group):
    fluent_name = ...
    child_names = ...
    center: center_cls = ...
    radius: radius_cls = ...
    inside: inside_cls = ...
    create_volume_surface: create_volume_surface_cls = ...
