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
from .rename import rename as rename_cls
from .list import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .initialize_5 import initialize as initialize_cls
from .duplicate import duplicate as duplicate_cls
from .set_as_current import set_as_current as set_as_current_cls
from .use_base_data import use_base_data as use_base_data_cls
from .export_design_table import export_design_table as export_design_table_cls
from .import_design_table import import_design_table as import_design_table_cls
from .parametric_studies_child import parametric_studies_child


class parametric_studies(NamedObject[parametric_studies_child], _CreatableNamedObjectMixin[parametric_studies_child]):
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

    def initialize(self, project_filename: str):
        """
        Start Parametric Study.
        
        Parameters
        ----------
            project_filename : str
                'project_filename' child.
        
        """

    def duplicate(self, copy_design_points: bool):
        """
        Duplicate Parametric Study.
        
        Parameters
        ----------
            copy_design_points : bool
                'copy_design_points' child.
        
        """

    def set_as_current(self, study_name: str):
        """
        Set As Current Study.
        
        Parameters
        ----------
            study_name : str
                'study_name' child.
        
        """

    def use_base_data(self, ):
        """
        Use Base Data.
        """

    def export_design_table(self, filepath: str):
        """
        Export Design Point Table.
        
        Parameters
        ----------
            filepath : str
                'filepath' child.
        
        """

    def import_design_table(self, filepath: str, delete_existing: bool):
        """
        Import Design Point Table.
        
        Parameters
        ----------
            filepath : str
                'filepath' child.
            delete_existing : bool
                'delete_existing' child.
        
        """

    child_object_type = ...
