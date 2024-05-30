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

from .type import type as type_cls
from .two_dim_space import two_dim_space as two_dim_space_cls
from .velocity_formulation import velocity_formulation as velocity_formulation_cls
from .time import time as time_cls

class solver(Group):
    fluent_name = ...
    child_names = ...
    type: type_cls = ...
    two_dim_space: two_dim_space_cls = ...
    velocity_formulation: velocity_formulation_cls = ...
    time: time_cls = ...
