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
from .joule_heat_parameter import joule_heat_parameter as joule_heat_parameter_cls
from .transient_setup import transient_setup as transient_setup_cls
from .file_saving_frequency import file_saving_frequency as file_saving_frequency_cls
from .lti_rom_generation import lti_rom_generation as lti_rom_generation_cls
from .add_rom_parameter import add_rom_parameter as add_rom_parameter_cls
from .rom_data_creator import rom_data_creator as rom_data_creator_cls
from .list_rom_parameter import list_rom_parameter as list_rom_parameter_cls
from .delete_rom_parameter import delete_rom_parameter as delete_rom_parameter_cls

class rom_tool_kit(Group):
    fluent_name = ...
    child_names = ...
    rom_type: rom_type_cls = ...
    joule_heat_parameter: joule_heat_parameter_cls = ...
    transient_setup: transient_setup_cls = ...
    file_saving_frequency: file_saving_frequency_cls = ...
    lti_rom_generation: lti_rom_generation_cls = ...
    command_names = ...

    def add_rom_parameter(self, parameter_type: int, entity_list: List[str], individual_or_group: bool, individual_value: bool, group_value: Union[float, str], value_list: List[Union[float, str]]):
        """
        'add_rom_parameter' command.
        
        Parameters
        ----------
            parameter_type : int
                'parameter_type' child.
            entity_list : typing.List[str]
                'entity_list' child.
            individual_or_group : bool
                'individual_or_group' child.
            individual_value : bool
                'individual_value' child.
            group_value : real
                'group_value' child.
            value_list : typing.List[real]
                'value_list' child.
        
        """

    def rom_data_creator(self, ):
        """
        Non-conformal Interface Matching.
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

