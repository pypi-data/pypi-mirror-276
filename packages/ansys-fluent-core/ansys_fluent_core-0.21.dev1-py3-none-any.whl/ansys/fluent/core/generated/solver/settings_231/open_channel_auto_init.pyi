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

from .boundary_thread import boundary_thread as boundary_thread_cls
from .flat_init import flat_init as flat_init_cls
from .wavy_surface_init import wavy_surface_init as wavy_surface_init_cls

class open_channel_auto_init(Group):
    fluent_name = ...
    child_names = ...
    boundary_thread: boundary_thread_cls = ...
    flat_init: flat_init_cls = ...
    wavy_surface_init: wavy_surface_init_cls = ...
