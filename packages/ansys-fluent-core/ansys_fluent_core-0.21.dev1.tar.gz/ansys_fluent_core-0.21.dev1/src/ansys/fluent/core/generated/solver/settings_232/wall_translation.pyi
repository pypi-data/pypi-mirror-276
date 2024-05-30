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

from .list_properties_1 import list_properties as list_properties_cls
from .axis_direction_child import axis_direction_child


class wall_translation(ListObject[axis_direction_child]):
    fluent_name = ...
    command_names = ...

    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        
        Parameters
        ----------
            object_at : int
                'object_at' child.
        
        """

    child_object_type = ...
