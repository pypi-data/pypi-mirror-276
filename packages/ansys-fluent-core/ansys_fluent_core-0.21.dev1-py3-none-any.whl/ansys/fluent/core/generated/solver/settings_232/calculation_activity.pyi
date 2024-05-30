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

from .execute_commands import execute_commands as execute_commands_cls
from .solution_animations import solution_animations as solution_animations_cls
from .poor_mesh_numerics import poor_mesh_numerics as poor_mesh_numerics_cls
from .enable_strategy import enable_strategy as enable_strategy_cls
from .copy_modification import copy_modification as copy_modification_cls
from .delete_modification import delete_modification as delete_modification_cls
from .enable_modification import enable_modification as enable_modification_cls
from .disable_modification import disable_modification as disable_modification_cls
from .import_modifications import import_modifications as import_modifications_cls
from .export_modifications import export_modifications as export_modifications_cls
from .continue_strategy_execution import continue_strategy_execution as continue_strategy_execution_cls

class calculation_activity(Group):
    fluent_name = ...
    child_names = ...
    execute_commands: execute_commands_cls = ...
    solution_animations: solution_animations_cls = ...
    poor_mesh_numerics: poor_mesh_numerics_cls = ...
    command_names = ...

    def enable_strategy(self, enable: bool):
        """
        Specify whether automatic initialization and case modification should be enabled.
        
        Parameters
        ----------
            enable : bool
                'enable' child.
        
        """

    def copy_modification(self, mod_name: str):
        """
        Copy a single case modification.
        
        Parameters
        ----------
            mod_name : str
                'mod_name' child.
        
        """

    def delete_modification(self, mod_name: str):
        """
        Delete a single case modification.
        
        Parameters
        ----------
            mod_name : str
                'mod_name' child.
        
        """

    def enable_modification(self, mod_name: str):
        """
        Enable a single defined case modification.
        
        Parameters
        ----------
            mod_name : str
                'mod_name' child.
        
        """

    def disable_modification(self, mod_name: str):
        """
        Disable a single defined case modification.
        
        Parameters
        ----------
            mod_name : str
                'mod_name' child.
        
        """

    def import_modifications(self, filename: str):
        """
        Import a list of case modifications from a tsv file.
        
        Parameters
        ----------
            filename : str
                'filename' child.
        
        """

    def export_modifications(self, command_list: List[str], filename: str):
        """
        Export all case modifications to a tsv file.
        
        Parameters
        ----------
            command_list : typing.List[str]
                'command_list' child.
            filename : str
                'filename' child.
        
        """

    def continue_strategy_execution(self, ):
        """
        Continue execution of the automatic initialization and case modification strategy defined at present.
        """

