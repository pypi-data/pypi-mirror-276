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

from .data_sampling import data_sampling as data_sampling_cls
from .sampling_interval import sampling_interval as sampling_interval_cls
from .statistics_shear_stress import statistics_shear_stress as statistics_shear_stress_cls
from .statistics_heat_flux import statistics_heat_flux as statistics_heat_flux_cls
from .wall_statistics import wall_statistics as wall_statistics_cls
from .force_statistics import force_statistics as force_statistics_cls
from .time_statistics_dpm import time_statistics_dpm as time_statistics_dpm_cls
from .species_list import species_list as species_list_cls
from .statistics_mixture_fraction import statistics_mixture_fraction as statistics_mixture_fraction_cls
from .statistics_reaction_progress import statistics_reaction_progress as statistics_reaction_progress_cls
from .save_cff_unsteady_statistics import save_cff_unsteady_statistics as save_cff_unsteady_statistics_cls
from .setup_unsteady_statistics import setup_unsteady_statistics as setup_unsteady_statistics_cls

class data_sampling(Group):
    fluent_name = ...
    child_names = ...
    data_sampling: data_sampling_cls = ...
    sampling_interval: sampling_interval_cls = ...
    statistics_shear_stress: statistics_shear_stress_cls = ...
    statistics_heat_flux: statistics_heat_flux_cls = ...
    wall_statistics: wall_statistics_cls = ...
    force_statistics: force_statistics_cls = ...
    time_statistics_dpm: time_statistics_dpm_cls = ...
    species_list: species_list_cls = ...
    statistics_mixture_fraction: statistics_mixture_fraction_cls = ...
    statistics_reaction_progress: statistics_reaction_progress_cls = ...
    save_cff_unsteady_statistics: save_cff_unsteady_statistics_cls = ...
    command_names = ...

    def setup_unsteady_statistics(self, udf_cf_names: List[str]):
        """
        'setup_unsteady_statistics' command.
        
        Parameters
        ----------
            udf_cf_names : typing.List[str]
                'udf_cf_names' child.
        
        """

