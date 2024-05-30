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

from .interpolate_flow_cp import interpolate_flow_cp as interpolate_flow_cp_cls
from .interpolate_flow_density import interpolate_flow_density as interpolate_flow_density_cls
from .interpolate_flow_solution_gradients import interpolate_flow_solution_gradients as interpolate_flow_solution_gradients_cls
from .interpolate_flow_viscosity import interpolate_flow_viscosity as interpolate_flow_viscosity_cls
from .interpolate_temperature import interpolate_temperature as interpolate_temperature_cls
from .zero_nodal_velocities_on_walls import zero_nodal_velocities_on_walls as zero_nodal_velocities_on_walls_cls

class interpolation(Group):
    fluent_name = ...
    child_names = ...
    interpolate_flow_cp: interpolate_flow_cp_cls = ...
    interpolate_flow_density: interpolate_flow_density_cls = ...
    interpolate_flow_solution_gradients: interpolate_flow_solution_gradients_cls = ...
    interpolate_flow_viscosity: interpolate_flow_viscosity_cls = ...
    interpolate_temperature: interpolate_temperature_cls = ...
    zero_nodal_velocities_on_walls: zero_nodal_velocities_on_walls_cls = ...
