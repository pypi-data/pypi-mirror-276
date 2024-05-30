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

from .axes_3 import axes as axes_cls
from .main import main as main_cls
from .scale_5 import scale as scale_cls
from .text_1 import text as text_cls
from .video import video as video_cls
from .xy import xy as xy_cls
from .logo import logo as logo_cls
from .ruler_1 import ruler as ruler_cls
from .logo_color import logo_color as logo_color_cls
from .aspect_ratio import aspect_ratio as aspect_ratio_cls
from .open_window import open_window as open_window_cls
from .set_window import set_window as set_window_cls
from .set_window_by_name import set_window_by_name as set_window_by_name_cls
from .close_window import close_window as close_window_cls
from .close_window_by_name import close_window_by_name as close_window_by_name_cls

class windows(Group):
    fluent_name = ...
    child_names = ...
    axes: axes_cls = ...
    main: main_cls = ...
    scale: scale_cls = ...
    text: text_cls = ...
    video: video_cls = ...
    xy: xy_cls = ...
    logo: logo_cls = ...
    ruler: ruler_cls = ...
    logo_color: logo_color_cls = ...
    command_names = ...

    def aspect_ratio(self, width: Union[float, str], height: Union[float, str]):
        """
        Set the aspect ratio of the active window.
        
        Parameters
        ----------
            width : real
                'width' child.
            height : real
                'height' child.
        
        """

    def open_window(self, window_id: int):
        """
        Open a user graphics window.
        
        Parameters
        ----------
            window_id : int
                'window_id' child.
        
        """

    def set_window(self, window_id: int):
        """
        Set a user graphics window to be the active window.
        
        Parameters
        ----------
            window_id : int
                'window_id' child.
        
        """

    def set_window_by_name(self, window_name: str):
        """
        Set a reserved graphics window to be the active window by its name.
        
        Parameters
        ----------
            window_name : str
                'window_name' child.
        
        """

    def close_window(self, window_id: int):
        """
        Close a user graphics window.
        
        Parameters
        ----------
            window_id : int
                'window_id' child.
        
        """

    def close_window_by_name(self, window_name: str):
        """
        Close a reserved graphics window by its name.
        
        Parameters
        ----------
            window_name : str
                'window_name' child.
        
        """

