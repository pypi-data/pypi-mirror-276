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

from .set_units import set_units as set_units_cls
from .set_unit_system import set_unit_system as set_unit_system_cls

class units(Group):
    fluent_name = ...
    command_names = ...

    def set_units(self, quantity: str, units_name: str, scale_factor: Union[float, str], offset: Union[float, str]):
        """
        Set unit conversion factors.
        
        Parameters
        ----------
            quantity : str
                'quantity' child.
            units_name : str
                'units_name' child.
            scale_factor : real
                'scale_factor' child.
            offset : real
                'offset' child.
        
        """

    def set_unit_system(self, unit_system: str):
        """
        To apply standard set of units to all quantities.
        
        Parameters
        ----------
            unit_system : str
                'unit_system' child.
        
        """

