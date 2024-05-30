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

from .scalar_parameters import scalar_parameters as scalar_parameters_cls
from .coupled_parameters import coupled_parameters as coupled_parameters_cls
from .flexible_cycle_paramters import flexible_cycle_paramters as flexible_cycle_paramters_cls
from .options_1 import options as options_cls

class algebric_mg_controls(Group):
    fluent_name = ...
    child_names = ...
    scalar_parameters: scalar_parameters_cls = ...
    coupled_parameters: coupled_parameters_cls = ...
    flexible_cycle_paramters: flexible_cycle_paramters_cls = ...
    options: options_cls = ...
