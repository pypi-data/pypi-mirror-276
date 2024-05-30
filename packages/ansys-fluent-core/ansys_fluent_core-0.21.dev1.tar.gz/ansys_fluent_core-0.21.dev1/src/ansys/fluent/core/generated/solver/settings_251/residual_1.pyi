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

from .equation_for_residual import equation_for_residual as equation_for_residual_cls
from .threshold import threshold as threshold_cls

class residual(Group):
    fluent_name = ...
    child_names = ...
    equation_for_residual: equation_for_residual_cls = ...
    threshold: threshold_cls = ...
