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

from .fixed_cycle_parameters_1 import fixed_cycle_parameters as fixed_cycle_parameters_cls
from .coarsening_parameters_1 import coarsening_parameters as coarsening_parameters_cls
from .smoother_type_1 import smoother_type as smoother_type_cls

class coupled_parameters(Group):
    fluent_name = ...
    child_names = ...
    fixed_cycle_parameters: fixed_cycle_parameters_cls = ...
    coarsening_parameters: coarsening_parameters_cls = ...
    smoother_type: smoother_type_cls = ...
