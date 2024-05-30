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
from .minimum_4 import minimum as minimum_cls
from .maximum_4 import maximum as maximum_cls
from .volume_2 import volume as volume_cls
from .volume_average import volume_average as volume_average_cls
from .volume_integral import volume_integral as volume_integral_cls

class volume_integrals(Group):
    fluent_name = ...
    command_names = ...

    def mass_average(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print mass-average of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            volumes : typing.List[str]
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def mass_integral(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print mass-weighted integral of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            volumes : typing.List[str]
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def mass(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print total mass of specified cell zones.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            volumes : typing.List[str]
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def sum(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print sum of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            volumes : typing.List[str]
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def twopisum(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print sum of scalar over specified cell zones multiplied by 2*Pi.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            volumes : typing.List[str]
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def minimum(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print minimum of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            volumes : typing.List[str]
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def maximum(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print maximum of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            volumes : typing.List[str]
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def volume(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print total volume of specified cell zones.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            volumes : typing.List[str]
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def volume_average(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print volume-weighted average of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            volumes : typing.List[str]
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def volume_integral(self, cell_zones: List[str], volumes: List[str], cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print volume integral of scalar over specified cell zones.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Volume id/name.
            volumes : typing.List[str]
                UTL Volume name.
            cell_function : str
                Specify Field.
            current_domain : str
                Select the domain.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

