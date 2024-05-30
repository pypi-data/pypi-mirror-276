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

from .proximity_tolerance import proximity_tolerance as proximity_tolerance_cls
from .set_default_name_prefix import set_default_name_prefix as set_default_name_prefix_cls
from .set_minimum_area_percentage import set_minimum_area_percentage as set_minimum_area_percentage_cls
from .pairing_between_different_cell_zones_only import pairing_between_different_cell_zones_only as pairing_between_different_cell_zones_only_cls
from .pairing_between_interface_zones_only import pairing_between_interface_zones_only as pairing_between_interface_zones_only_cls
from .keep_empty_interface import keep_empty_interface as keep_empty_interface_cls
from .naming_option import naming_option as naming_option_cls
from .set_one_to_one_pairing_tolerance import set_one_to_one_pairing_tolerance as set_one_to_one_pairing_tolerance_cls

class auto_options(Group):
    fluent_name = ...
    child_names = ...
    proximity_tolerance: proximity_tolerance_cls = ...
    set_default_name_prefix: set_default_name_prefix_cls = ...
    set_minimum_area_percentage: set_minimum_area_percentage_cls = ...
    pairing_between_different_cell_zones_only: pairing_between_different_cell_zones_only_cls = ...
    pairing_between_interface_zones_only: pairing_between_interface_zones_only_cls = ...
    keep_empty_interface: keep_empty_interface_cls = ...
    command_names = ...

    def naming_option(self, option: str, change_all_one_to_one_interfaces_names: bool):
        """
        Specify whether or not to include an informative suffix to the mesh interface name.
        
        Parameters
        ----------
            option : str
                (0) basic:           name-prefix:##
        (1) name-based:      name-prefix:##:interface_name1::interface_name2
        (2) ID-based:        name-prefix:##:interface_ID1::interface-ID2
        (3) adjacency-based: name-prefix:##:cell_zone_name1::cell_zone_name2.
            change_all_one_to_one_interfaces_names : bool
                Apply the new naming option to existing one-to-one mesh interfaces?.
        
        """

    def set_one_to_one_pairing_tolerance(self, adjustable_tolerance: bool, length_factor: Union[float, str]):
        """
        Set one-to-one adjustable tolerance.
        
        Parameters
        ----------
            adjustable_tolerance : bool
                Enable/disable one-to-one adjustable tolerance.
            length_factor : real
                Enter a valid number for length factor.
        
        """

