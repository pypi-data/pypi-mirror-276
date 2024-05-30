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

from .enabled_39 import enabled as enabled_cls
from .initialization_method import initialization_method as initialization_method_cls
from .case_modification import case_modification as case_modification_cls
from .automatic_initialization import automatic_initialization as automatic_initialization_cls
from .execute_strategy import execute_strategy as execute_strategy_cls
from .enable_strategy import enable_strategy as enable_strategy_cls
from .copy_modification import copy_modification as copy_modification_cls
from .delete_modification import delete_modification as delete_modification_cls
from .enable_modification import enable_modification as enable_modification_cls
from .disable_modification import disable_modification as disable_modification_cls
from .import_modifications import import_modifications as import_modifications_cls
from .export_modifications import export_modifications as export_modifications_cls
from .continue_strategy_execution import continue_strategy_execution as continue_strategy_execution_cls

class case_modification(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    initialization_method: initialization_method_cls = ...
    case_modification: case_modification_cls = ...
    command_names = ...

    def automatic_initialization(self, initialization_type: str, data_file_name: str, init_from_solution: str, data_file_name2: str):
        """
        Define how the case is to be initialized automatically.
        
        Parameters
        ----------
            initialization_type : str
                'initialization_type' child.
            data_file_name : str
                'data_file_name' child.
            init_from_solution : str
                'init_from_solution' child.
            data_file_name2 : str
                'data_file_name2' child.
        
        """

    def execute_strategy(self, save_mode: str, continue_with_current_mesh: bool, discard_all_data: bool):
        """
        Execute the automatic initialization and case modification strategy defined at present .
        
        Parameters
        ----------
            save_mode : str
                'save_mode' child.
            continue_with_current_mesh : bool
                Reloading of the upstream mesh data is desired. Is it needed to continue with currently loaded mesh?.
            discard_all_data : bool
                'discard_all_data' child.
        
        """

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

    def export_modifications(self, command_list: List[str], filename_2: str):
        """
        Export all case modifications to a tsv file.
        
        Parameters
        ----------
            command_list : typing.List[str]
                'command_list' child.
            filename_2 : str
                'filename' child.
        
        """

    def continue_strategy_execution(self, ):
        """
        Continue execution of the automatic initialization and case modification strategy defined at present.
        """

