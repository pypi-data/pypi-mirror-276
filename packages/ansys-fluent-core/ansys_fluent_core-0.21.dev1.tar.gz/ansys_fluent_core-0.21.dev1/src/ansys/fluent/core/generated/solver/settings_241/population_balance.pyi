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

from .moments import moments as moments_cls
from .number_density import number_density as number_density_cls

class population_balance(Group):
    fluent_name = ...
    command_names = ...

    def moments(self, surface_list: List[str], volume_list: List[str], num_of_moments: int, write_to_file: bool, filename: str):
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
            filename : str
                'filename' child.
        
        """

    def number_density(self, report_type: str, disc_output_type: str, qmom_output_type: str, smm_output_type: str, surface_list: List[str], volume_list: List[str], num_dens_func: str, dia_upper_limit: Union[float, str], file_name: str):
        """
        'number_density' command.
        
        Parameters
        ----------
            report_type : str
                'report_type' child.
            disc_output_type : str
                'disc_output_type' child.
            qmom_output_type : str
                'qmom_output_type' child.
            smm_output_type : str
                'smm_output_type' child.
            surface_list : typing.List[str]
                Select surface.
            volume_list : typing.List[str]
                Enter cell zone name list.
            num_dens_func : str
                'num_dens_func' child.
            dia_upper_limit : real
                'dia_upper_limit' child.
            file_name : str
                'file_name' child.
        
        """

