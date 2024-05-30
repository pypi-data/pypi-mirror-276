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

from .limit_pressure_correction_gradient import limit_pressure_correction_gradient as limit_pressure_correction_gradient_cls

class skewness_correction(Group):
    fluent_name = ...
    child_names = ...
    limit_pressure_correction_gradient: limit_pressure_correction_gradient_cls = ...
