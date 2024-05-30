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

from .function_of import function_of as function_of_cls
from .coefficients import coefficients as coefficients_cls

class polynomial(Group):
    fluent_name = ...
    child_names = ...
    function_of: function_of_cls = ...
    coefficients: coefficients_cls = ...
