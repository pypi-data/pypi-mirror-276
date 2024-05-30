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

from .fmg_courant_number import fmg_courant_number as fmg_courant_number_cls
from .enable_fmg_verbose import enable_fmg_verbose as enable_fmg_verbose_cls
from .viscous_terms import viscous_terms as viscous_terms_cls
from .species_reactions import species_reactions as species_reactions_cls
from .turbulent_viscosity_ratio_3 import turbulent_viscosity_ratio as turbulent_viscosity_ratio_cls
from .fmg_initialize import fmg_initialize as fmg_initialize_cls
from .customize import customize as customize_cls
from .reset_to_defaults import reset_to_defaults as reset_to_defaults_cls

class fmg(Group):
    fluent_name = ...
    child_names = ...
    fmg_courant_number: fmg_courant_number_cls = ...
    enable_fmg_verbose: enable_fmg_verbose_cls = ...
    viscous_terms: viscous_terms_cls = ...
    species_reactions: species_reactions_cls = ...
    turbulent_viscosity_ratio: turbulent_viscosity_ratio_cls = ...
    command_names = ...

    def fmg_initialize(self, ):
        """
        Initialize using the full-multigrid initialization (FMG).
        """

    def customize(self, multi_level_grid: int, residual_reduction: List[Union[float, str]], cycle_count: List[Union[float, str]]):
        """
        Enter FMG customization menu.
        
        Parameters
        ----------
            multi_level_grid : int
                Enter number of multigrid levels.
            residual_reduction : typing.List[real]
                Enter number of residual reduction levels.
            cycle_count : typing.List[real]
                Enter number of cycles.
        
        """

    def reset_to_defaults(self, ):
        """
        'reset_to_defaults' command.
        """

