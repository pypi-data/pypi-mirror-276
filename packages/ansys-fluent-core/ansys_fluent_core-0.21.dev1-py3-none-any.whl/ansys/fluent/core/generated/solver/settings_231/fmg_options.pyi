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

from .viscous_terms import viscous_terms as viscous_terms_cls
from .species_reactions import species_reactions as species_reactions_cls
from .set_turbulent_viscosity_ratio import set_turbulent_viscosity_ratio as set_turbulent_viscosity_ratio_cls

class fmg_options(Group):
    fluent_name = ...
    child_names = ...
    viscous_terms: viscous_terms_cls = ...
    species_reactions: species_reactions_cls = ...
    set_turbulent_viscosity_ratio: set_turbulent_viscosity_ratio_cls = ...
