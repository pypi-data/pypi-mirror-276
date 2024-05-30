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

from .number_density import number_density as number_density_cls
from .moments import moments as moments_cls

class population_balance(Group):
    fluent_name = ...
    child_names = ...
    number_density: number_density_cls = ...
    command_names = ...

    def moments(self, surface_list: List[str], volume_list: List[str], num_of_moments: int, write_to_file: bool, filename_2: str):
        """
        Set moments for population balance.
        
        Parameters
        ----------
            surface_list : typing.List[str]
                Select surface.
            volume_list : typing.List[str]
                Enter cell zone name list.
            num_of_moments : int
                'num_of_moments' child.
            write_to_file : bool
                'write_to_file' child.
            filename_2 : str
                'filename' child.
        
        """

