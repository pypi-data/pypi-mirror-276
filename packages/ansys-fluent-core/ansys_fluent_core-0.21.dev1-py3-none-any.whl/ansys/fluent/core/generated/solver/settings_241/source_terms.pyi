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

from .linearization import linearization as linearization_cls
from .impl_mom_cplg_enabled import impl_mom_cplg_enabled as impl_mom_cplg_enabled_cls
from .impl_cplg_enabled import impl_cplg_enabled as impl_cplg_enabled_cls
from .linear_change_enabled import linear_change_enabled as linear_change_enabled_cls
from .reset_sources_at_timestep import reset_sources_at_timestep as reset_sources_at_timestep_cls
from .underrelaxation_factor import underrelaxation_factor as underrelaxation_factor_cls
from .time_accurate_sources_enabled import time_accurate_sources_enabled as time_accurate_sources_enabled_cls

class source_terms(Group):
    fluent_name = ...
    child_names = ...
    linearization: linearization_cls = ...
    impl_mom_cplg_enabled: impl_mom_cplg_enabled_cls = ...
    impl_cplg_enabled: impl_cplg_enabled_cls = ...
    linear_change_enabled: linear_change_enabled_cls = ...
    reset_sources_at_timestep: reset_sources_at_timestep_cls = ...
    underrelaxation_factor: underrelaxation_factor_cls = ...
    time_accurate_sources_enabled: time_accurate_sources_enabled_cls = ...
