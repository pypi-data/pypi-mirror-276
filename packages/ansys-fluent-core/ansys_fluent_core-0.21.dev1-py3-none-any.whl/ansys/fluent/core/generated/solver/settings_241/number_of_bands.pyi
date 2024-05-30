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

from .set_all_interfaces import set_all_interfaces as set_all_interfaces_cls
from .set_specific_interface import set_specific_interface as set_specific_interface_cls

class number_of_bands(Group):
    fluent_name = ...
    child_names = ...
    set_all_interfaces: set_all_interfaces_cls = ...
    command_names = ...

    def set_specific_interface(self, interface_number: int, bands: int):
        """
        Set number of band to be used for mixing.
        
        Parameters
        ----------
            interface_number : int
                Set number of band to be used for mixing.
            bands : int
                Set number of band to be used for mixing.
        
        """

