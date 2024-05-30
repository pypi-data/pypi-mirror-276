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
from .set_one_to_one_pairing_tolerance import set_one_to_one_pairing_tolerance as set_one_to_one_pairing_tolerance_cls
from .pairing_between_different_cell_zones_only import pairing_between_different_cell_zones_only as pairing_between_different_cell_zones_only_cls
from .pairing_between_interface_zones_only import pairing_between_interface_zones_only as pairing_between_interface_zones_only_cls
from .keep_empty_interface import keep_empty_interface as keep_empty_interface_cls
from .naming_option import naming_option as naming_option_cls

class auto_options(Group):
    fluent_name = ...
    child_names = ...
    proximity_tolerance: proximity_tolerance_cls = ...
    set_default_name_prefix: set_default_name_prefix_cls = ...
    set_one_to_one_pairing_tolerance: set_one_to_one_pairing_tolerance_cls = ...
    pairing_between_different_cell_zones_only: pairing_between_different_cell_zones_only_cls = ...
    pairing_between_interface_zones_only: pairing_between_interface_zones_only_cls = ...
    keep_empty_interface: keep_empty_interface_cls = ...
    command_names = ...

    def naming_option(self, option: int, change_all_o2o_si_names: bool):
        """
        Specify whether or not to include an informative suffix to the mesh interface name.
        
        Parameters
        ----------
            option : int
                'option' child.
            change_all_o2o_si_names : bool
                'change_all_o2o_si_names' child.
        
        """

