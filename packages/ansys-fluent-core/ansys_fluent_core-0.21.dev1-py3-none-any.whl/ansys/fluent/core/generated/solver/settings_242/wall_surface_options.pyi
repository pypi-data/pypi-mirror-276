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

from .heat_of_surface_reactions import heat_of_surface_reactions as heat_of_surface_reactions_cls
from .mass_deposition_source import mass_deposition_source as mass_deposition_source_cls
from .reaction_diffusion_balance import reaction_diffusion_balance as reaction_diffusion_balance_cls
from .surface_reaction_aggresiveness_factor import surface_reaction_aggresiveness_factor as surface_reaction_aggresiveness_factor_cls
from .surface_reaction_rate_temperature_factor import surface_reaction_rate_temperature_factor as surface_reaction_rate_temperature_factor_cls
from .surface_reaction_solid_fraction import surface_reaction_solid_fraction as surface_reaction_solid_fraction_cls

class wall_surface_options(Group):
    fluent_name = ...
    child_names = ...
    heat_of_surface_reactions: heat_of_surface_reactions_cls = ...
    mass_deposition_source: mass_deposition_source_cls = ...
    reaction_diffusion_balance: reaction_diffusion_balance_cls = ...
    surface_reaction_aggresiveness_factor: surface_reaction_aggresiveness_factor_cls = ...
    surface_reaction_rate_temperature_factor: surface_reaction_rate_temperature_factor_cls = ...
    surface_reaction_solid_fraction: surface_reaction_solid_fraction_cls = ...
