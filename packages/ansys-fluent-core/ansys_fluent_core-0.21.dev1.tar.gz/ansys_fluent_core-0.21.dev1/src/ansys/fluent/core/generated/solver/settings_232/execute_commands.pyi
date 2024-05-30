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

from .enable_14 import enable as enable_cls
from .disable_1 import disable as disable_cls
from .copy_3 import copy as copy_cls
from .delete_2 import delete as delete_cls
from .export_1 import export as export_cls
from .import__1 import import_ as import__cls

class execute_commands(Group):
    fluent_name = ...
    command_names = ...

    def enable(self, command_name: str):
        """
        Enable an execute-command.
        
        Parameters
        ----------
            command_name : str
                'command_name' child.
        
        """

    def disable(self, command_name: str):
        """
        Disable an execute-command.
        
        Parameters
        ----------
            command_name : str
                'command_name' child.
        
        """

    def copy(self, command_name: str):
        """
        Copy an execute-command.
        
        Parameters
        ----------
            command_name : str
                'command_name' child.
        
        """

    def delete(self, command_name: str):
        """
        Delete an execute-command.
        
        Parameters
        ----------
            command_name : str
                'command_name' child.
        
        """

    def export(self, command_name: List[str], tsv_file_name: str):
        """
        Export execute-commands to a TSV file.
        
        Parameters
        ----------
            command_name : typing.List[str]
                'command_name' child.
            tsv_file_name : str
                'tsv_file_name' child.
        
        """

    def import_(self, tsv_file_name: str):
        """
        Import execute-commands from a TSV file.
        
        Parameters
        ----------
            tsv_file_name : str
                'tsv_file_name' child.
        
        """

