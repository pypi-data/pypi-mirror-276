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

from .change_type import change_type as change_type_cls
from .axis_child import axis_child


class axis(NamedObject[axis_child], _CreatableNamedObjectMixin[axis_child]):
    fluent_name = ...
    command_names = ...

    def change_type(self, zone_list: List[str], new_type: str):
        """
        'change_type' command.
        
        Parameters
        ----------
            zone_list : typing.List[str]
                'zone_list' child.
            new_type : str
                'new_type' child.
        
        """

    child_object_type = ...
