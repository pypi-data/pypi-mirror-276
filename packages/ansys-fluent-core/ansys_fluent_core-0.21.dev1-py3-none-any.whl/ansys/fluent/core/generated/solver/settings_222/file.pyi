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

from .read import read as read_cls
from .replace_mesh import replace_mesh as replace_mesh_cls
from .write import write as write_cls
from .parametric_project import parametric_project as parametric_project_cls

class file(Group):
    fluent_name = ...
    command_names = ...

    def read(self, file_type: str, file_name: str):
        """
        'read' command.
        
        Parameters
        ----------
            file_type : str
                'file_type' child.
            file_name : str
                'file_name' child.
        
        """

    def replace_mesh(self, file_name: str):
        """
        'replace_mesh' command.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def write(self, file_type: str, file_name: str):
        """
        'write' command.
        
        Parameters
        ----------
            file_type : str
                'file_type' child.
            file_name : str
                'file_name' child.
        
        """

    def parametric_project(self, ):
        """
        'parametric_project' child.
        """

