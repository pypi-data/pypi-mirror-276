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

from .new import new as new_cls
from .open import open as open_cls
from .save import save as save_cls
from .save_as import save_as as save_as_cls
from .save_as_copy import save_as_copy as save_as_copy_cls
from .archive import archive as archive_cls

class parametric_project(Group):
    fluent_name = ...
    command_names = ...

    def new(self, project_filename: str):
        """
        Create New Project.
        
        Parameters
        ----------
            project_filename : str
                'project_filename' child.
        
        """

    def open(self, project_filename_1: str, load_case: bool):
        """
        Open project.
        
        Parameters
        ----------
            project_filename_1 : str
                'project_filename' child.
            load_case : bool
                'load_case' child.
        
        """

    def save(self, ):
        """
        Save Project.
        """

    def save_as(self, project_filename: str):
        """
        Save As Project.
        
        Parameters
        ----------
            project_filename : str
                'project_filename' child.
        
        """

    def save_as_copy(self, project_filename: str, convert_to_managed: bool):
        """
        Save As Project.
        
        Parameters
        ----------
            project_filename : str
                'project_filename' child.
            convert_to_managed : bool
                'convert_to_managed' child.
        
        """

    def archive(self, archive_name: str):
        """
        Archive Project.
        
        Parameters
        ----------
            archive_name : str
                'archive_name' child.
        
        """

