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

from .rom_type import rom_type as rom_type_cls
from .transient_setup import transient_setup as transient_setup_cls
from .file_saving_frequency import file_saving_frequency as file_saving_frequency_cls
from .joule_heat_parameter import joule_heat_parameter as joule_heat_parameter_cls
from .add_rom_parameter import add_rom_parameter as add_rom_parameter_cls
from .rom_data_creator import rom_data_creator as rom_data_creator_cls
from .create_journal_file import create_journal_file as create_journal_file_cls
from .list_rom_parameter import list_rom_parameter as list_rom_parameter_cls
from .delete_rom_parameter import delete_rom_parameter as delete_rom_parameter_cls

class rom_data_creator_tool(Group):
    fluent_name = ...
    child_names = ...
    rom_type: rom_type_cls = ...
    transient_setup: transient_setup_cls = ...
    file_saving_frequency: file_saving_frequency_cls = ...
    joule_heat_parameter: joule_heat_parameter_cls = ...
    command_names = ...

    def add_rom_parameter(self, parameter_type: str, entity_list: List[str], group_value: Union[float, str], individual_or_group: bool, individual_value: bool, value_list: List[Union[float, str]]):
        """
        Add parameter command.
        
        Parameters
        ----------
            parameter_type : str
                Set parameter type.
            entity_list : typing.List[str]
                Entity list name.
            group_value : real
                Set group value.
            individual_or_group : bool
                Set as-group option.
            individual_value : bool
                Set individual value for different entities in the group.
            value_list : typing.List[real]
                Set values for the different entities in the group.
        
        """

    def rom_data_creator(self, rom_type: int):
        """
        ROM data creator.
        
        Parameters
        ----------
            rom_type : int
                ROM type in ROM-data creator.
        
        """

    def create_journal_file(self, rom_type: int):
        """
        Create journal file.
        
        Parameters
        ----------
            rom_type : int
                ROM type in the ROM simulation.
        
        """

    def list_rom_parameter(self, ):
        """
        Print all ROM-related paramters.
        """

    def delete_rom_parameter(self, parameter_names: List[str]):
        """
        Delete ROM-related paramters.
        
        Parameters
        ----------
            parameter_names : typing.List[str]
                Set deleted parameter lists.
        
        """

