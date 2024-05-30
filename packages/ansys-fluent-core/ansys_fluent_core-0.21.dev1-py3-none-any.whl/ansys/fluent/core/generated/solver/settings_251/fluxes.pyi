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

from .mass_flow_1 import mass_flow as mass_flow_cls
from .heat_transfer import heat_transfer as heat_transfer_cls
from .heat_transfer_sensible import heat_transfer_sensible as heat_transfer_sensible_cls
from .radiation_heat_transfer import radiation_heat_transfer as radiation_heat_transfer_cls
from .film_mass_flow import film_mass_flow as film_mass_flow_cls
from .film_heat_transfer import film_heat_transfer as film_heat_transfer_cls
from .electric_current import electric_current as electric_current_cls
from .pressure_work_1 import pressure_work as pressure_work_cls
from .viscous_work import viscous_work as viscous_work_cls

class fluxes(Group):
    fluent_name = ...
    command_names = ...

    def mass_flow(self, domain: str, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print mass flow rate at inlets and outlets.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : typing.List[str]
                Enter zone name list.
            physics : typing.List[str]
                'physics' child.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def heat_transfer(self, domain: str, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : typing.List[str]
                Enter zone name list.
            physics : typing.List[str]
                'physics' child.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def heat_transfer_sensible(self, domain: str, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print sensible heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : typing.List[str]
                Enter zone name list.
            physics : typing.List[str]
                'physics' child.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def radiation_heat_transfer(self, domain: str, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print radiation heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : typing.List[str]
                Enter zone name list.
            physics : typing.List[str]
                'physics' child.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def film_mass_flow(self, domain: str, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print film mass flow rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : typing.List[str]
                Enter zone name list.
            physics : typing.List[str]
                'physics' child.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def film_heat_transfer(self, domain: str, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print film heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : typing.List[str]
                Enter zone name list.
            physics : typing.List[str]
                'physics' child.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def electric_current(self, domain: str, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print electric current rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : typing.List[str]
                Enter zone name list.
            physics : typing.List[str]
                'physics' child.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def pressure_work(self, domain: str, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print pressure work rate at moving boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : typing.List[str]
                Enter zone name list.
            physics : typing.List[str]
                'physics' child.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

    def viscous_work(self, domain: str, zones: List[str], physics: List[str], write_to_file: bool, file_name: str, append_data: bool):
        """
        Print viscous work rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
            zones : typing.List[str]
                Enter zone name list.
            physics : typing.List[str]
                'physics' child.
            write_to_file : bool
                Choose whether or not to write to a file.
            file_name : str
                Enter the name you want the file saved with.
            append_data : bool
                Choose whether or not to append data to existing file.
        
        """

