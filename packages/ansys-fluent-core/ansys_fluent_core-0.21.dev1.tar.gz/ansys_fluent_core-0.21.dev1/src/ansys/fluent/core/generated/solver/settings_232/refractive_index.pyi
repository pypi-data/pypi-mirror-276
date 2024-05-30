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

from .option_10 import option as option_cls
from .value_1 import value as value_cls
from .gray_band_coefficients import gray_band_coefficients as gray_band_coefficients_cls

class refractive_index(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    value: value_cls = ...
    gray_band_coefficients: gray_band_coefficients_cls = ...
