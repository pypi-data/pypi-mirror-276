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

from .boundary_choice import boundary_choice as boundary_choice_cls
from .report_3 import report as report_cls
from .write_to_file_5 import write_to_file as write_to_file_cls

class reporting(Group):
    fluent_name = ...
    child_names = ...
    boundary_choice: boundary_choice_cls = ...
    command_names = ...

    def report(self, ):
        """
        Boundary condition sensitivity report in console.
        """

    def write_to_file(self, file_name: str, append_data: bool):
        """
        Write report to file.
        
        Parameters
        ----------
            file_name : str
                File name.
            append_data : bool
                Append data to file.
        
        """

