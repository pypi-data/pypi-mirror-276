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

from .create_1 import create_1 as create_1_cls
from .duplicate_1 import duplicate as duplicate_cls
from .load_case_data import load_case_data as load_case_data_cls
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
