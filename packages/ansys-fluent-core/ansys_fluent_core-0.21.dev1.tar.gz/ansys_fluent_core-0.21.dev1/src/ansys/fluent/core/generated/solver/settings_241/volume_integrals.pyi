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

from .mass_average import mass_average as mass_average_cls
from .mass_integral import mass_integral as mass_integral_cls
from .mass import mass as mass_cls
from .sum_1 import sum as sum_cls
from .twopisum import twopisum as twopisum_cls
from .minimum_2 import minimum as minimum_cls
from .maximum_2 import maximum as maximum_cls
from .volume_2 import volume as volume_cls
from .volume_average import volume_average as volume_average_cls
from .volume_integral import volume_integral as volume_integral_cls

class volume_integrals(Group):
    fluent_name = ...
    command_names = ...

    def mass_average(self, cell_zones: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print mass-average of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            cell_function : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def mass_integral(self, cell_zones: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print mass-weighted integral of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            cell_function : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def mass(self, cell_zones: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print total mass of specified cell zones.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            cell_function : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def sum(self, cell_zones: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print sum of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            cell_function : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def twopisum(self, cell_zones: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print sum of scalar over specified cell zones multiplied by 2*Pi.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            cell_function : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def minimum(self, cell_zones: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print minimum of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            cell_function : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def maximum(self, cell_zones: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print maximum of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            cell_function : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def volume(self, cell_zones: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print total volume of specified cell zones.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            cell_function : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def volume_average(self, cell_zones: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print volume-weighted average of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            cell_function : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def volume_integral(self, cell_zones: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print volume integral of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            cell_function : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

