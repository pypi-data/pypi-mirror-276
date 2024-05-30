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

from .display import display as display_cls
from .mesh_child_1 import mesh_child


class mesh(NamedObject[mesh_child], _CreatableNamedObjectMixin[mesh_child]):
    fluent_name = ...
    command_names = ...

    def display(self, object_name: str):
        """
        'display' command.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        
        """

    child_object_type = ...
