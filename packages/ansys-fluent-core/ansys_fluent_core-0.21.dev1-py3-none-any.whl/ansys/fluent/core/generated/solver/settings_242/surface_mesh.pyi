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

from .delete import delete as delete_cls
from .display import display as display_cls
from .read_2 import read as read_cls

class surface_mesh(Group):
    fluent_name = ...
    command_names = ...

    def delete(self, surface: str):
        """
        Delete surface mesh.
        
        Parameters
        ----------
            surface : str
                'surface' child.
        
        """

    def display(self, ):
        """
        Display surface meshes.
        """

    def read(self, filename: str, unit: str):
        """
        Read surface meshes.
        
        Parameters
        ----------
            filename : str
                'filename' child.
            unit : str
                'unit' child.
        
        """

