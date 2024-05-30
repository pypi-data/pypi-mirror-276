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

from .vof_smooth_options import vof_smooth_options as vof_smooth_options_cls
from .calculate_patch import calculate_patch as calculate_patch_cls

class patch(Group):
    fluent_name = ...
    child_names = ...
    vof_smooth_options: vof_smooth_options_cls = ...
    command_names = ...

    def calculate_patch(self, domain: str, cell_zones: List[str], register_id: List[str], variable: str, patch_velocity: bool, use_custom_field_function: bool, custom_field_function_name: str, value: Union[float, str]):
        """
        Patch a value for a flow variable in the domain.
        
        Parameters
        ----------
            domain : str
                'domain' child.
            cell_zones : typing.List[str]
                'cell_zones' child.
            register_id : typing.List[str]
                'register_id' child.
            variable : str
                'variable' child.
            patch_velocity : bool
                'patch_velocity' child.
            use_custom_field_function : bool
                'use_custom_field_function' child.
            custom_field_function_name : str
                'custom_field_function_name' child.
            value : real
                'value' child.
        
        """

