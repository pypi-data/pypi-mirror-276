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

from .name_1 import name as name_cls
from .title import title as title_cls
from .temporary import temporary as temporary_cls
from .graphics_objects import graphics_objects as graphics_objects_cls
from .display_state_name import display_state_name as display_state_name_cls
from .display_3 import display as display_cls

class scene_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    title: title_cls = ...
    temporary: temporary_cls = ...
    graphics_objects: graphics_objects_cls = ...
    display_state_name: display_state_name_cls = ...
    command_names = ...

    def display(self, ):
        """
        'display' command.
        """

