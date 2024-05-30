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

from .multiphase_options import multiphase_options as multiphase_options_cls
from .turbulence_multiphase_models import turbulence_multiphase_models as turbulence_multiphase_models_cls
from .rsm_multiphase_models import rsm_multiphase_models as rsm_multiphase_models_cls
from .subgrid_turbulence_contribution_aiad import subgrid_turbulence_contribution_aiad as subgrid_turbulence_contribution_aiad_cls

class multiphase_turbulence(Group):
    fluent_name = ...
    child_names = ...
    multiphase_options: multiphase_options_cls = ...
    turbulence_multiphase_models: turbulence_multiphase_models_cls = ...
    rsm_multiphase_models: rsm_multiphase_models_cls = ...
    subgrid_turbulence_contribution_aiad: subgrid_turbulence_contribution_aiad_cls = ...
