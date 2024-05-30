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

from .wall_treatment import wall_treatment as wall_treatment_cls
from .user_defined import user_defined as user_defined_cls
from .enhanced_wall_treatment_options import enhanced_wall_treatment_options as enhanced_wall_treatment_options_cls
from .wall_omega_treatment import wall_omega_treatment as wall_omega_treatment_cls

class near_wall_treatment(Group):
    fluent_name = ...
    child_names = ...
    wall_treatment: wall_treatment_cls = ...
    user_defined: user_defined_cls = ...
    enhanced_wall_treatment_options: enhanced_wall_treatment_options_cls = ...
    wall_omega_treatment: wall_omega_treatment_cls = ...
