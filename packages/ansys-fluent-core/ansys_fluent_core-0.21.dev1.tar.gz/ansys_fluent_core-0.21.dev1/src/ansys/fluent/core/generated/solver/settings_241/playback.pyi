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
from .current_animation import current_animation as current_animation_cls
from .read_animation_file import read_animation_file as read_animation_file_cls
from .write_animation import write_animation as write_animation_cls
from .stored_view import stored_view as stored_view_cls
from .delete_5 import delete as delete_cls
from .play import play as play_cls

class playback(Group):
    fluent_name = ...
    child_names = ...
    set_custom_frames: set_custom_frames_cls = ...
    video: video_cls = ...
    current_animation: current_animation_cls = ...
    command_names = ...

    def read_animation_file(self, animation_file_name: str):
        """
        Read new animation from file or already-defined animations.
        
        Parameters
        ----------
            animation_file_name : str
                'animation_file_name' child.
        
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

    def delete(self, delete_all: bool, name: str):
        """
        Delete animation sequence.
        
        Parameters
        ----------
            delete_all : bool
                Yes: "Delete all animations", no: "Delete single animation.".
            name : str
                Select animation to delete.
        
        """

    def play(self, player: str, start_frame: int, end_frame: int, increment: int, playback_mode: str, speed: int):
        """
        Play the selected animation.
        
        Parameters
        ----------
            player : str
                Enter the Player Operation.
            start_frame : int
                Start Frame Number.
            end_frame : int
                Start Frame Number.
            increment : int
                Skip frame while playing.
            playback_mode : str
                Enter the playback mode.
            speed : int
                Animation play speed.
        
        """

