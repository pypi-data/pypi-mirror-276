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

from .expected_changes import expected_changes as expected_changes_cls
from .optimal_displacements import optimal_displacements as optimal_displacements_cls
from .stl_surfaces import stl_surfaces as stl_surfaces_cls

class export(Group):
    fluent_name = ...
    command_names = ...

    def expected_changes(self, file_name: str, append_data: bool):
        """
        Write expected changes to file.
        
        Parameters
        ----------
            file_name : str
                Expected changes report name.
            append_data : bool
                Append data to file.
        
        """

    def optimal_displacements(self, file_name: str):
        """
        Export the computed optimal displacements.
        
        Parameters
        ----------
            file_name : str
                Displacements file name.
        
        """

    def stl_surfaces(self, surfaces: List[str], file_name: str):
        """
        Export specified surfaces from 3D cases as an .stl file.
        
        Parameters
        ----------
            surfaces : typing.List[str]
                Specify surfaces to be exported as .stl file.
            file_name : str
                Export specified surfaces from 3D cases as an .stl file.
        
        """

