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

from .gravity import gravity as gravity_cls
from .real_gas_state import real_gas_state as real_gas_state_cls
from .operating_pressure import operating_pressure as operating_pressure_cls
from .reference_pressure_location import reference_pressure_location as reference_pressure_location_cls
from .reference_pressure_method import reference_pressure_method as reference_pressure_method_cls
from .operating_density import operating_density as operating_density_cls
from .operating_temperature import operating_temperature as operating_temperature_cls
from .used_ref_pressure_location import used_ref_pressure_location as used_ref_pressure_location_cls
from .use_inlet_temperature_for_operating_density import use_inlet_temperature_for_operating_density as use_inlet_temperature_for_operating_density_cls

class operating_conditions(Group):
    fluent_name = ...
    child_names = ...
    gravity: gravity_cls = ...
    real_gas_state: real_gas_state_cls = ...
    operating_pressure: operating_pressure_cls = ...
    reference_pressure_location: reference_pressure_location_cls = ...
    reference_pressure_method: reference_pressure_method_cls = ...
    operating_density: operating_density_cls = ...
    operating_temperature: operating_temperature_cls = ...
    command_names = ...

    def used_ref_pressure_location(self, ):
        """
        See the actual coordinates of reference pressure used.
        """

    def use_inlet_temperature_for_operating_density(self, zone_name: str):
        """
        Use Inlet Temperature to calculate Opearating Density.
        
        Parameters
        ----------
            zone_name : str
                'zone_name' child.
        
        """

