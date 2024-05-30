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

from .set_custom_frames_1 import set_custom_frames as set_custom_frames_cls
from .read_animation import read_animation as read_animation_cls
from .write_animation_1 import write_animation as write_animation_cls
from .add_keyframe import add_keyframe as add_keyframe_cls
from .delete_keyframe import delete_keyframe as delete_keyframe_cls
from .delete_all_keyframes import delete_all_keyframes as delete_all_keyframes_cls
from .play_1 import play as play_cls

class scene_animation(Group):
    fluent_name = ...
    child_names = ...
    set_custom_frames: set_custom_frames_cls = ...
    command_names = ...

    def read_animation(self, file_name_1: str):
        """
        'read_animation' command.
        
        Parameters
        ----------
            file_name_1 : str
                'file_name' child.
        
        """

    def write_animation(self, format_name: str, file_name: str):
        """
        Write keyframe Animation file.
        
        Parameters
        ----------
            format_name : str
                'format_name' child.
            file_name : str
                'file_name' child.
        
        """

    def add_keyframe(self, key: int):
        """
        Add keyframe.
        
        Parameters
        ----------
            key : int
                'key' child.
        
        """

    def delete_keyframe(self, key: int):
        """
        Delete a keyframe.
        
        Parameters
        ----------
            key : int
                'key' child.
        
        """

    def delete_all_keyframes(self, ):
        """
        Delete all keyframes.
        """

    def play(self, start_keyframe: int, end_keyframe: int, increment: int):
        """
        Play keyframe animation.
        
        Parameters
        ----------
            start_keyframe : int
                Set start keyframe.
            end_keyframe : int
                Set end keyframe.
            increment : int
                Set increment.
        
        """

