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

from .enable_turb_damping import enable_turb_damping as enable_turb_damping_cls
from .turb_damping_factor import turb_damping_factor as turb_damping_factor_cls

class turbulence_damping(Group):
    fluent_name = ...
    child_names = ...
    enable_turb_damping: enable_turb_damping_cls = ...
    turb_damping_factor: turb_damping_factor_cls = ...
