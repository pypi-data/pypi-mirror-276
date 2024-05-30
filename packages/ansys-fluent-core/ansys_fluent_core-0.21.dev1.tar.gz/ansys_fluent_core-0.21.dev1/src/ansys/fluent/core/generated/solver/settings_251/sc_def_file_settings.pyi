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

from .enable_auto_creation_of_scp_file import enable_auto_creation_of_scp_file as enable_auto_creation_of_scp_file_cls
from .write_sc_file import write_sc_file as write_sc_file_cls

class sc_def_file_settings(Group):
    fluent_name = ...
    child_names = ...
    enable_auto_creation_of_scp_file: enable_auto_creation_of_scp_file_cls = ...
    command_names = ...

    def write_sc_file(self, file_name: str):
        """
        Write a Fluent Input File for System Coupling.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
        
        """

