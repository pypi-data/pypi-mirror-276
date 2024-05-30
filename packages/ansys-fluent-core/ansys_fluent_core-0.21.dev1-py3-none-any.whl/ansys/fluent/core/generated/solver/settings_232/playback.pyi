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

from .set_custom_frames import set_custom_frames as set_custom_frames_cls
from .video_1 import video as video_cls
from .read_animation import read_animation as read_animation_cls
from .write_animation import write_animation as write_animation_cls
from .stored_view import stored_view as stored_view_cls

class playback(Group):
    fluent_name = ...
    child_names = ...
    set_custom_frames: set_custom_frames_cls = ...
    video: video_cls = ...
    command_names = ...

    def read_animation(self, read_from_file: bool, animation_file_name: str, select_from_available: bool, animation_name: str):
        """
        Read new animation from file or already-defined animations.
        
        Parameters
        ----------
            read_from_file : bool
                'read_from_file' child.
            animation_file_name : str
                'animation_file_name' child.
            select_from_available : bool
                'select_from_available' child.
            animation_name : str
                'animation_name' child.
        
        """

    def write_animation(self, format_name: str):
        """
        Write animation sequence to the file.
        
        Parameters
        ----------
            format_name : str
                'format_name' child.
        
        """

    def stored_view(self, view: bool):
        """
        Play the 3D animation sequence using the view stored in the sequence.
        
        Parameters
        ----------
            view : bool
                Yes: "Stored View", no: "Different View".
        
        """

