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

    def calculate_patch(self, domain: str, cell_zones: List[str], registers: List[str], variable: str, reference_frame: str, use_custom_field_function: bool, custom_field_function_name: str, value: Union[float, str]):
        """
        Patch a value for a flow variable in the domain.
        
        Parameters
        ----------
            domain : str
                Enter domain.
            cell_zones : typing.List[str]
                Enter cell zone.
            registers : typing.List[str]
                Enter register.
            variable : str
                Enter variable.
            reference_frame : str
                Select velocity Reference Frame.
            use_custom_field_function : bool
                Enable/disable custom field function for patching.
            custom_field_function_name : str
                Enter custom function.
            value : real
                Enter patch value.
        
        """

