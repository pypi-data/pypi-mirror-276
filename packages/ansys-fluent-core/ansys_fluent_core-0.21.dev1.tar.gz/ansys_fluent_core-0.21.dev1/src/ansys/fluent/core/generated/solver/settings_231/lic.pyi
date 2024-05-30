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

from .display_1 import display as display_cls
from .copy_3 import copy as copy_cls
from .add_to_graphics import add_to_graphics as add_to_graphics_cls
from .clear_history import clear_history as clear_history_cls
from .lic_child import lic_child


class lic(NamedObject[lic_child], _CreatableNamedObjectMixin[lic_child]):
    fluent_name = ...
    command_names = ...

    def display(self, object_name: str):
        """
        Display graphics object.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        
        """

    def copy(self, from_name: str, new_name: str):
        """
        Copy graphics object.
        
        Parameters
        ----------
            from_name : str
                'from_name' child.
            new_name : str
                'new_name' child.
        
        """

    def add_to_graphics(self, object_name: str):
        """
        Add graphics object to existing graphics.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        
        """

    def clear_history(self, object_name: str):
        """
        Clear object history.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        
        """

    child_object_type = ...
