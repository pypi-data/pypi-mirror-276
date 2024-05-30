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

from .computed_heat_rejection import computed_heat_rejection as computed_heat_rejection_cls
from .inlet_temperature import inlet_temperature as inlet_temperature_cls
from .outlet_temperature import outlet_temperature as outlet_temperature_cls
from .mass_flow_rate_3 import mass_flow_rate as mass_flow_rate_cls
from .specific_heat_5 import specific_heat as specific_heat_cls

class heat_exchanger(Group):
    fluent_name = ...
    command_names = ...

    def computed_heat_rejection(self, heat_exchanger: str, fluid_zone: str, boundary_zone: str, report_type: str, write_to_file: bool, file_name: str, append_file: bool):
        """
        Print total heat rejection.
        
        Parameters
        ----------
            heat_exchanger : str
                'heat_exchanger' child.
            fluid_zone : str
                'fluid_zone' child.
            boundary_zone : str
                Enter face zone name.
            report_type : str
                'report_type' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_file : bool
                'append_file' child.
        
        """

    def inlet_temperature(self, heat_exchanger: str, fluid_zone: str, boundary_zone: str, report_type: str, write_to_file: bool, file_name: str, append_file: bool):
        """
        Print inlet temperature.
        
        Parameters
        ----------
            heat_exchanger : str
                'heat_exchanger' child.
            fluid_zone : str
                'fluid_zone' child.
            boundary_zone : str
                Enter face zone name.
            report_type : str
                'report_type' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_file : bool
                'append_file' child.
        
        """

    def outlet_temperature(self, heat_exchanger: str, fluid_zone: str, boundary_zone: str, report_type: str, write_to_file: bool, file_name: str, append_file: bool):
        """
        Print outlet temperature.
        
        Parameters
        ----------
            heat_exchanger : str
                'heat_exchanger' child.
            fluid_zone : str
                'fluid_zone' child.
            boundary_zone : str
                Enter face zone name.
            report_type : str
                'report_type' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_file : bool
                'append_file' child.
        
        """

    def mass_flow_rate(self, heat_exchanger: str, fluid_zone: str, boundary_zone: str, report_type: str, write_to_file: bool, file_name: str, append_file: bool):
        """
        Print mass flow rate.
        
        Parameters
        ----------
            heat_exchanger : str
                'heat_exchanger' child.
            fluid_zone : str
                'fluid_zone' child.
            boundary_zone : str
                Enter face zone name.
            report_type : str
                'report_type' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_file : bool
                'append_file' child.
        
        """

    def specific_heat(self, heat_exchanger: str, fluid_zone: str, boundary_zone: str, report_type: str, write_to_file: bool, file_name: str, append_file: bool):
        """
        Print fluid's specific heat.
        
        Parameters
        ----------
            heat_exchanger : str
                'heat_exchanger' child.
            fluid_zone : str
                'fluid_zone' child.
            boundary_zone : str
                Enter face zone name.
            report_type : str
                'report_type' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_file : bool
                'append_file' child.
        
        """

