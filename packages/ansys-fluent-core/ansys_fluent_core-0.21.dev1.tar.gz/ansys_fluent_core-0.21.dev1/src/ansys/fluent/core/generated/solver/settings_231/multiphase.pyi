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

from .models import models as models_cls
from .vaporization_pressure import vaporization_pressure as vaporization_pressure_cls
from .non_condensable_gas import non_condensable_gas as non_condensable_gas_cls
from .liquid_surface_tension import liquid_surface_tension as liquid_surface_tension_cls
from .bubble_number_density import bubble_number_density as bubble_number_density_cls
from .number_of_phases import number_of_phases as number_of_phases_cls
from .number_of_eulerian_discrete_phases import number_of_eulerian_discrete_phases as number_of_eulerian_discrete_phases_cls

class multiphase(Group):
    fluent_name = ...
    child_names = ...
    models: models_cls = ...
    vaporization_pressure: vaporization_pressure_cls = ...
    non_condensable_gas: non_condensable_gas_cls = ...
    liquid_surface_tension: liquid_surface_tension_cls = ...
    bubble_number_density: bubble_number_density_cls = ...
    number_of_phases: number_of_phases_cls = ...
    number_of_eulerian_discrete_phases: number_of_eulerian_discrete_phases_cls = ...
