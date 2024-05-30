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

from .on_all_interfaces import on_all_interfaces as on_all_interfaces_cls
from .on_specified_interface import on_specified_interface as on_specified_interface_cls

class number_of_bands(Group):
    fluent_name = ...
    command_names = ...

    def on_all_interfaces(self, bands: int):
        """
        Maximum number of bands to be employed at all the mixing planes.
        
        Parameters
        ----------
            bands : int
                Maximum number of band counts.
        
        """

    def on_specified_interface(self, interface_name: str, bands: int):
        """
        Maximum number of bands to be employed at the specified mixing plane interface.
        
        Parameters
        ----------
            interface_name : str
                Define the mixing plane interface to specify band count.
            bands : int
                Maximum number of band counts.
        
        """

