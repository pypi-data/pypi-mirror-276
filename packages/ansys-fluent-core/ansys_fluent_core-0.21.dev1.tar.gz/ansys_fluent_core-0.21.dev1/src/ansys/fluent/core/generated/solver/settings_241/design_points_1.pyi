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

from .delete_1 import delete as delete_cls
from .list import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .create_1 import create_1 as create_1_cls
from .duplicate_1 import duplicate as duplicate_cls
from .load_case_data import load_case_data as load_case_data_cls
from .set_as_current_1 import set_as_current as set_as_current_cls
from .delete_design_points import delete_design_points as delete_design_points_cls
from .save_journals import save_journals as save_journals_cls
from .clear_generated_data import clear_generated_data as clear_generated_data_cls
from .update_current import update_current as update_current_cls
from .update_all import update_all as update_all_cls
from .update_selected import update_selected as update_selected_cls
from .design_points_child import design_points_child


class design_points(NamedObject[design_points_child], _CreatableNamedObjectMixin[design_points_child]):
    fluent_name = ...
    command_names = ...

    def delete(self, name_list: List[str]):
        """
        Delete selected objects.
        
        Parameters
        ----------
            name_list : typing.List[str]
                Select objects to be deleted.
        
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

    def create_1(self, write_data: bool, capture_simulation_report_data: bool):
        """
        Add new Design Point.
        
        Parameters
        ----------
            write_data : bool
                'write_data' child.
            capture_simulation_report_data : bool
                'capture_simulation_report_data' child.
        
        """

    def duplicate(self, design_point: str):
        """
        Duplicate Design Point.
        
        Parameters
        ----------
            design_point : str
                'design_point' child.
        
        """

    def load_case_data(self, ):
        """
        Loads relevant case/data file for current design point.
        """

    def set_as_current(self, design_point: str):
        """
        Set current design point.
        
        Parameters
        ----------
            design_point : str
                'design_point' child.
        
        """

    def delete_design_points(self, design_points: List[str]):
        """
        Delete Design Points.
        
        Parameters
        ----------
            design_points : typing.List[str]
                'design_points' child.
        
        """

    def save_journals(self, separate_journals: bool):
        """
        Save Journals.
        
        Parameters
        ----------
            separate_journals : bool
                'separate_journals' child.
        
        """

    def clear_generated_data(self, design_points: List[str]):
        """
        Clear Generated Data.
        
        Parameters
        ----------
            design_points : typing.List[str]
                'design_points' child.
        
        """

    def update_current(self, ):
        """
        Update Current Design Point.
        """

    def update_all(self, ):
        """
        Update All Design Point.
        """

    def update_selected(self, design_points: List[str]):
        """
        Update Selected Design Points.
        
        Parameters
        ----------
            design_points : typing.List[str]
                'design_points' child.
        
        """

    child_object_type = ...
