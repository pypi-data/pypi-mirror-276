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

from .minimum import minimum as minimum_cls
from .maximum import maximum as maximum_cls
from .coefficients_1 import coefficients as coefficients_cls

class piecewise_polynomial_child(Group):
    fluent_name = ...
    child_names = ...
    minimum: minimum_cls = ...
    maximum: maximum_cls = ...
    coefficients: coefficients_cls = ...
