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
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .display_frame import display_frame as display_frame_cls
from .hide_frame import hide_frame as hide_frame_cls
from .reference_frames_child import reference_frames_child


class reference_frames(NamedObject[reference_frames_child], _CreatableNamedObjectMixin[reference_frames_child]):
    fluent_name = ...
    command_names = ...

    def list(self, ):
        """
        'list' command.
        """

    def list_properties(self, object_name: str):
        """
        'list_properties' command.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        
        """

    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        
        Parameters
        ----------
            from_ : str
                'from' child.
            to : str
                'to' child.
        
        """

    def display_frame(self, name: str):
        """
        Display Reference Frame.
        
        Parameters
        ----------
            name : str
                'name' child.
        
        """

    def hide_frame(self, name: str):
        """
        Hide Reference Frame.
        
        Parameters
        ----------
            name : str
                'name' child.
        
        """

    child_object_type = ...
