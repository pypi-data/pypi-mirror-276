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

from .enable_velocity_limiting import enable_velocity_limiting as enable_velocity_limiting_cls
from .set_velocity_and_vof_cutoffs import set_velocity_and_vof_cutoffs as set_velocity_and_vof_cutoffs_cls
from .set_damping_strengths import set_damping_strengths as set_damping_strengths_cls
from .set_velocity_cutoff import set_velocity_cutoff as set_velocity_cutoff_cls
from .set_damping_strength import set_damping_strength as set_damping_strength_cls
from .verbosity_5 import verbosity as verbosity_cls

class velocity_limiting_treatment(Group):
    fluent_name = ...
    child_names = ...
    enable_velocity_limiting: enable_velocity_limiting_cls = ...
    set_velocity_and_vof_cutoffs: set_velocity_and_vof_cutoffs_cls = ...
    set_damping_strengths: set_damping_strengths_cls = ...
    set_velocity_cutoff: set_velocity_cutoff_cls = ...
    set_damping_strength: set_damping_strength_cls = ...
    verbosity: verbosity_cls = ...
