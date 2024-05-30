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

from .option import option as option_cls
from .constant import constant as constant_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
from .polynomial import polynomial as polynomial_cls
from .user_defined_3 import user_defined as user_defined_cls

class direct_solar_irradiation(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    constant: constant_cls = ...
    piecewise_linear: piecewise_linear_cls = ...
    polynomial: polynomial_cls = ...
    user_defined: user_defined_cls = ...
