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

from .under_relaxation_factor import under_relaxation_factor as under_relaxation_factor_cls
from .verbosity_6 import verbosity as verbosity_cls

class target_mass_flow_rate_settings(Group):
    fluent_name = ...
    child_names = ...
    under_relaxation_factor: under_relaxation_factor_cls = ...
    verbosity: verbosity_cls = ...
