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

from .mass_flow_specification import mass_flow_specification as mass_flow_specification_cls
from .mass_flow_rate_1 import mass_flow_rate as mass_flow_rate_cls
from .mass_flux import mass_flux as mass_flux_cls
from .participates_in_solar_ray_tracing import participates_in_solar_ray_tracing as participates_in_solar_ray_tracing_cls
from .solar_transmissivity_factor import solar_transmissivity_factor as solar_transmissivity_factor_cls

class recirculation_outlet(Group):
    fluent_name = ...
    child_names = ...
    mass_flow_specification: mass_flow_specification_cls = ...
    mass_flow_rate: mass_flow_rate_cls = ...
    mass_flux: mass_flux_cls = ...
    participates_in_solar_ray_tracing: participates_in_solar_ray_tracing_cls = ...
    solar_transmissivity_factor: solar_transmissivity_factor_cls = ...
