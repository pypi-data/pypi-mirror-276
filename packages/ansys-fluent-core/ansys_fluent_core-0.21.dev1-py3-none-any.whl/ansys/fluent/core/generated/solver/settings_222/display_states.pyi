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

from .list import list as list_cls
from .use_active import use_active as use_active_cls
from .restore_state import restore_state as restore_state_cls
from .copy import copy as copy_cls
from .read_1 import read as read_cls
from .write_1 import write as write_cls
from .display_states_child import display_states_child


class display_states(NamedObject[display_states_child], _CreatableNamedObjectMixin[display_states_child]):
    fluent_name = ...
    command_names = ...

    def list(self, ):
        """
        'list' command.
        """

    def use_active(self, state_name: str):
        """
        'use_active' command.
        
        Parameters
        ----------
            state_name : str
                'state_name' child.
        
        """

    def restore_state(self, state_name: str):
        """
        Apply a display state to the active window.
        
        Parameters
        ----------
            state_name : str
                'state_name' child.
        
        """

    def copy(self, state_name: str):
        """
        Create a new display state with settings copied from an existing display state.
        
        Parameters
        ----------
            state_name : str
                'state_name' child.
        
        """

    def read(self, file_name: str):
        """
        Read display states from a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def write(self, file_name: str, state_name: List[str]):
        """
        Write display states to a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            state_name : typing.List[str]
                'state_name' child.
        
        """

    child_object_type = ...
