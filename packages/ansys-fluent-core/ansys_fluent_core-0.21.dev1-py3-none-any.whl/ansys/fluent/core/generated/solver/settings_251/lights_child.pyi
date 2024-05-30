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

from .on import on as on_cls
from .rgb import rgb as rgb_cls
from .direction_4 import direction as direction_cls
from .set_direction_from_view_vector import set_direction_from_view_vector as set_direction_from_view_vector_cls

class lights_child(Group):
    fluent_name = ...
    child_names = ...
    on: on_cls = ...
    rgb: rgb_cls = ...
    direction: direction_cls = ...
    command_names = ...

    def set_direction_from_view_vector(self, ):
        """
        'set_direction_from_view_vector' command.
        """

