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

from .name_8 import name as name_cls
from .uid import uid as uid_cls
from .options_17 import options as options_cls
from .plot_direction import plot_direction as plot_direction_cls
from .x_axis_function_1 import x_axis_function as x_axis_function_cls
from .y_axis_function import y_axis_function as y_axis_function_cls
from .surfaces_list import surfaces_list as surfaces_list_cls
from .physics_1 import physics as physics_cls
from .geometry_7 import geometry as geometry_cls
from .surfaces_4 import surfaces as surfaces_cls
from .axes_1 import axes as axes_cls
from .curves_1 import curves as curves_cls
from .display_7 import display as display_cls
from .write_to_file import write_to_file as write_to_file_cls
from .read_from_file import read_from_file as read_from_file_cls
from .free_file_data import free_file_data as free_file_data_cls

class xy_plot_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    uid: uid_cls = ...
    options: options_cls = ...
    plot_direction: plot_direction_cls = ...
    x_axis_function: x_axis_function_cls = ...
    y_axis_function: y_axis_function_cls = ...
    surfaces_list: surfaces_list_cls = ...
    physics: physics_cls = ...
    geometry: geometry_cls = ...
    surfaces: surfaces_cls = ...
    axes: axes_cls = ...
    curves: curves_cls = ...
    command_names = ...

    def display(self, ):
        """
        Allows you to display the plot.
        """

    def write_to_file(self, filename_2: str):
        """
        Write data to a file.
        
        Parameters
        ----------
            filename_2 : str
                Type in the desired file name to save.
        
        """

    def read_from_file(self, filename: str):
        """
        Read data from file.
        
        Parameters
        ----------
            filename : str
                Enter file name.
        
        """

    def free_file_data(self, file_data_list: List[str]):
        """
        Free file-data.
        
        Parameters
        ----------
            file_data_list : typing.List[str]
                File-data to delete.
        
        """

