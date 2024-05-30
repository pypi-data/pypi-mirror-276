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

from .use_vapor_species_heat_capacity import use_vapor_species_heat_capacity as use_vapor_species_heat_capacity_cls

class diffusion_controlled(Group):
    fluent_name = ...
    child_names = ...
    use_vapor_species_heat_capacity: use_vapor_species_heat_capacity_cls = ...
