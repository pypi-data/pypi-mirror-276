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
from .animate_on import animate_on as animate_on_cls
from .frequency_of_1 import frequency_of as frequency_of_cls
from .frequency_3 import frequency as frequency_cls
from .flow_time_frequency import flow_time_frequency as flow_time_frequency_cls
from .last_flow_time import last_flow_time as last_flow_time_cls
from .append_filename_with import append_filename_with as append_filename_with_cls
from .storage_type import storage_type as storage_type_cls
from .storage_dir import storage_dir as storage_dir_cls
from .window_id import window_id as window_id_cls
from .view import view as view_cls
from .use_raytracing import use_raytracing as use_raytracing_cls
from .append_filename import append_filename as append_filename_cls
from .appended_flowtime_precision import appended_flowtime_precision as appended_flowtime_precision_cls
from .delete_1 import delete as delete_cls
from .rename import rename as rename_cls
from .list import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .display_2 import display as display_cls
from .copy_4 import copy as copy_cls
from .add_to_graphics import add_to_graphics as add_to_graphics_cls
from .clear_history import clear_history as clear_history_cls
from .solution_animations_child import solution_animations_child


class solution_animations(NamedObject[solution_animations_child], _CreatableNamedObjectMixin[solution_animations_child]):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    animate_on: animate_on_cls = ...
    frequency_of: frequency_of_cls = ...
    frequency: frequency_cls = ...
    flow_time_frequency: flow_time_frequency_cls = ...
    last_flow_time: last_flow_time_cls = ...
    append_filename_with: append_filename_with_cls = ...
    storage_type: storage_type_cls = ...
    storage_dir: storage_dir_cls = ...
    window_id: window_id_cls = ...
    view: view_cls = ...
    use_raytracing: use_raytracing_cls = ...
    append_filename: append_filename_cls = ...
    appended_flowtime_precision: appended_flowtime_precision_cls = ...
    command_names = ...

    def delete(self, name_list: List[str]):
        """
        Delete selected objects.
        
        Parameters
        ----------
            name_list : typing.List[str]
                Select objects to be deleted.
        
        """

    def rename(self, new: str, old: str):
        """
        Rename the object.
        
        Parameters
        ----------
            new : str
                New name for the object.
            old : str
                Select object to rename.
        
        """

    def list(self, ):
        """
        List the names of the objects.
        """

    def list_properties(self, object_name: str):
        """
        List active properties of the object.
        
        Parameters
        ----------
            object_name : str
                Select object for which properties are to be listed.
        
        """

    def make_a_copy(self, from_: str, to: str):
        """
        Create a copy of the object.
        
        Parameters
        ----------
            from_ : str
                Select the object to duplicate.
            to : str
                Specify the name of the new object.
        
        """

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
