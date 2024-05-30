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

from .number_of_coefficients import number_of_coefficients as number_of_coefficients_cls
from .coefficients import coefficients as coefficients_cls

class polynomial(Group):
    fluent_name = ...
    child_names = ...
    number_of_coefficients: number_of_coefficients_cls = ...
    coefficients: coefficients_cls = ...
