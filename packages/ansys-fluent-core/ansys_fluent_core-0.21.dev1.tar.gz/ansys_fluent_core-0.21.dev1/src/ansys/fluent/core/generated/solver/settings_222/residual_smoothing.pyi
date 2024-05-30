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

from .residual_smoothing_factor import residual_smoothing_factor as residual_smoothing_factor_cls
from .residual_smoothing_iteration import residual_smoothing_iteration as residual_smoothing_iteration_cls

class residual_smoothing(Group):
    fluent_name = ...
    child_names = ...
    residual_smoothing_factor: residual_smoothing_factor_cls = ...
    residual_smoothing_iteration: residual_smoothing_iteration_cls = ...
